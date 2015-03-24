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
            open_rate = price.bid
        else:
            # sell
            open_rate = price.ask

        # create
        return cls.objects.create(real=real,
                                  ai_board_id=ai_board_id,
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
        return list(cls.objects.filter(end_at__isnull=True).order_by('-created_at'))

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

    @property
    def currency_pair(self):
        return CurrencyPair(self._currency_pair)

    @property
    def side(self):
        return 'buy' if self.buy else 'sell'

    def open(self, price):
        """
        確定した注文を記録
        :param price: OrderApiModels
        """
        self.order_at = price.time
        _o = price.bid if self.buy else price.ask
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
        self.profit = self.get_profit(price)
        self.real_close_spread = price.cost_tick
        self.real_close_rate = price.ask if self.buy else price.bid  # 注文クローズなので反対売買する
        self.save()
        return self

    def get_profit(self, price):
        """
        利益を計算する
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
        if self.currency_pair != price.currency_pair:
            raise ValueError
        _price = price.bid if self.buy else price.ask

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