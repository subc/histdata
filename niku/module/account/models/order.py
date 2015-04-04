# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.functional import cached_property
import pytz
from module.genetic.models.parameter import OrderType
from module.rate import CurrencyPair


class Order(models.Model):
    # 日付
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_at = models.DateTimeField(default=None, null=True)
    end_at = models.DateTimeField(default=None, null=True, db_index=True)
    prev_rate_at = models.DateTimeField(default=None, null=True, db_index=True, help_text='直前のキャンドルの時間')
    # 基本情報
    ai_board_id = models.PositiveIntegerField()
    _currency_pair = models.PositiveIntegerField(default=None, null=True)
    ai_version = models.PositiveIntegerField(default=None, null=True, help_text='AIの取引世代')
    # 注文
    open_rate = models.FloatField(default=None, null=True, help_text='想定注文レート')
    buy = models.PositiveIntegerField()
    limit_tick = models.PositiveIntegerField()
    stop_limit_tick = models.PositiveIntegerField()
    spread = models.FloatField(help_text='発注決定時のスプレッド（発注時の値は取得できない）')
    # 本番更新
    real_open_rate = models.FloatField(default=None, null=True, help_text='約定時の注文レート')
    real_close_rate = models.FloatField(default=None, null=True, help_text='クローズ注文約定時のレート')
    real_limit_rate = models.FloatField(default=None, null=True)
    real_stop_limit_rate = models.FloatField(default=None, null=True)
    real = models.PositiveIntegerField(default=0, db_index=True)
    real_close_spread = models.FloatField(default=None, null=True, help_text='クローズ時のスプレッド')
    profit = models.FloatField(default=None, null=True)
    profit_tick = models.FloatField(default=None, null=True, help_text='最終実現損益tick')
    units = models.PositiveIntegerField(default=None, null=True, help_text='注文量')
    error = models.TextField(default=None, null=True)

    class Meta(object):
        app_label = 'account'

    @classmethod
    def pre_open(cls, ai_board, order, price, prev_rate_at):
        """
        仮注文発砲
        :param ai_board: AIBoard
        :param order: OrderAI
        :param price: PriceAPIModel
        :param prev_rate_at: datetime
        """
        real = ai_board.real
        ai_board_id = ai_board.id
        currency_pair = ai_board.currency_pair
        buy = 1 if order.order_type == OrderType.BUY else 0
        spread = price.cost_tick
        if buy:
            # buy
            open_rate = price.ask
        else:
            # sell
            open_rate = price.bid

        # create
        return cls.objects.create(real=real,
                                  ai_board_id=ai_board_id,
                                  ai_version=ai_board.version,
                                  _currency_pair=currency_pair,
                                  buy=buy,
                                  limit_tick=order.limit,
                                  stop_limit_tick=order.stop_limit,
                                  spread=spread,
                                  open_rate=open_rate,
                                  prev_rate_at=prev_rate_at,
                                  units=ai_board.units)

    @classmethod
    def get_open(cls):
        """
        オープンしている注文を返却
        :rtype :list of order
        """
        return list(cls.objects.filter(end_at__isnull=True,
                                       order_at__isnull=False).order_by('-created_at'))

    @classmethod
    def get_close(cls):
        """
        クローズしている注文を返却
        :rtype :list of order
        """
        return list(cls.objects.filter(end_at__isnull=False).order_by('-created_at'))

    @classmethod
    def get_close_by_scope(cls, start_delta, finish_delta):
        """
        クローズしている注文を返却
        :rtype :list of order
        """
        now = datetime.datetime.now(tz=pytz.utc)
        start = now - start_delta
        end = now - finish_delta
        print '{}:{}'.format(start, end)
        return list(cls.objects.filter(end_at__isnull=False,
                                       created_at__lte=start,
                                       created_at__gte=end).order_by('-created_at'))

    @classmethod
    def get_new_order(cls, ai_board_id):
        """
        最新のポジションを返却
        :param ai_board_id:int
        :rtype : Order
        """
        r = list(cls.objects.filter(ai_board_id=ai_board_id).order_by('-created_at'))
        if r:
            return r[0]
        return None

    @classmethod
    def confirm(cls, oanda_transaction):
        """
        正常に発注できている
        :param oanda_transaction: TransactionsAPIModel
        """
        # 注文タイプチェック
        if not oanda_transaction.market_order_create:
            return None

        if oanda_transaction.tradeId is None:
            return None

        # get
        order = cls.get_by_oanda_ticket_id(oanda_transaction.tradeId)
        if order is None:
            return None

        # 既に更新済み
        if order.is_confirm():
            return None

        # update
        order.confirm_at = oanda_transaction.time
        order.save()
        return order

    @classmethod
    def get_position_count(cls, ai_board_id):
        """
        ポジション数
        :param ai_board_id:
        :rtype : int
        """
        return cls.objects.filter(ai_board_id=ai_board_id,
                                  end_at__isnull=True).count()

    @classmethod
    def get_close_order_by_board(cls, board):
        """
        対象AIの決済済みポジションを返却
        :param board: AIBoard
        :rtype : list of Order
        """
        return list(cls.objects.filter(ai_board_id=board.id,
                                       ai_version=board.version,
                                       end_at__isnull=False))

    @classmethod
    def get_open_order_by_board(cls, board):
        """
        対象AIの未決済ポジションを返却
        :param board: AIBoard
        :rtype : list of Order
        """
        return list(cls.objects.filter(ai_board_id=board.id,
                                       ai_version=board.version,
                                       end_at__isnull=True))

    def open(self, price):
        """
        確定した注文を記録
        :param price: OrderApiModels
        """
        self.order_at = price.time
        _o = price.ask if self.buy else price.bid
        self.real_open_rate = _o
        if self.buy:
            self.real_limit_rate = _o + self.limit_tick * self.currency_pair.get_base_tick()
            self.real_stop_limit_rate = _o - self.stop_limit_tick * self.currency_pair.get_base_tick()
        else:
            self.real_limit_rate = _o - self.limit_tick * self.currency_pair.get_base_tick()
            self.real_stop_limit_rate = _o + self.stop_limit_tick * self.currency_pair.get_base_tick()
        self.save()

    def close(self, price):
        """
        利益確定の記録
        :param price: OrderApiModels
        """
        # 既に更新済み
        if self.is_close():
            return None

        # update
        self.end_at = price.time
        self.profit = self.calc_profit(price)
        self.real_close_spread = price.cost_tick
        self.real_close_rate = price.ask if self.buy else price.bid  # 注文クローズなので反対売買する
        self.profit_tick = self.get_profit_tick()
        self.save()
        return self

    def calc_profit(self, price):
        """
        クローズ直前のポジション利益を計算する
        :param price: OrderApiModels
        :rtype : float
        """
        if not self.can_close(price):
            raise ValueError
        _price = price.bid if self.buy else price.ask
        if self.buy:
            return self.currency_pair.units_to_yen(
                (_price - self.real_open_rate) / self.currency_pair.get_base_tick(), self.units)
        else:
            return self.currency_pair.units_to_yen(
                (self.real_open_rate - _price) / self.currency_pair.get_base_tick(), self.units)

    def get_current_profit(self, price):
        """
        オープンしているポジションの利益を計算する
        :param price: OrderApiModels
        :rtype : float
        """
        tick = self.get_current_profit_tick(price)
        return self.currency_pair.units_to_yen(tick, self.units)

    def get_current_profit_tick(self, price):
        """
        オープンしているポジションの利益を計算する
        :param price: OrderApiModels
        :rtype : float
        """
        if self.is_close():
            raise ValueError
        _price = price.bid if self.buy else price.ask
        if self.buy:
            return (_price - self.real_open_rate) / self.currency_pair.get_base_tick()
        else:
            return (self.real_open_rate - _price) / self.currency_pair.get_base_tick()

    def get_profit_tick(self):
        """
        利益tickを計算する
        :rtype : float
        """
        if not self.real_close_rate:
            raise ValueError
        if not self.real_open_rate:
            raise ValueError
        if self.buy:
            return (self.real_close_rate - self.real_open_rate) / self.currency_pair.get_base_tick()
        else:
            return (self.real_open_rate - self.real_close_rate) / self.currency_pair.get_base_tick()

    def set_order_error(self, e):
        """
        発注エラー
        """
        self.end_at = datetime.datetime.now(pytz.utc)
        self.error = str(e)
        self.save()

    def is_close(self):
        """
        クローズされていたらTrue
        :rtype :bool
        """
        return not self.profit is None

    def is_confirm(self):
        """
        confirm済みならTrue
        :rtype :bool
        """
        return bool(self.confirm_at)

    def can_close(self, price):
        """
        クローズできるならTrue
        :param price: PriceAPIModel
        :rtype : bool
        """
        # メンテ中なら売買しない
        if price.is_maintenance:
            return False

        # ティック差が大きすぎるときは売買しない
        if price.cost_tick >= 5:
            return False

        # 通過ペアの確認
        if self.currency_pair != price.currency_pair:
            raise ValueError

        # AIのシミュレーションと同じ様に、midのみを対象にして売買を決定する
        _price = price.mid

        if self.buy:
            if _price >= self.real_limit_rate:
                return True
            if _price <= self.real_stop_limit_rate:
                return True
        else:
            if _price <= self.real_limit_rate:
                return True
            if _price >= self.real_stop_limit_rate:
                return True
        return False

    @property
    def currency_pair(self):
        return CurrencyPair(self._currency_pair)

    @property
    def side(self):
        return 'buy' if self.buy else 'sell'

    @cached_property
    def board(self):
        from module.board.models.ai import AIBoard
        return AIBoard.get(self.ai_board_id)