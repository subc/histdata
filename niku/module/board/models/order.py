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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_at = models.DateTimeField(default=None, null=True)
    end_at = models.DateTimeField(default=None, null=True, db_index=True)
    prev_rate_at = models.DateTimeField(default=None, null=True, db_index=True, help_text='直前のキャンドルの時間')
    oanda_ticket_id = models.PositiveIntegerField(default=None, null=True)
    ai_board_id = models.PositiveIntegerField()
    _currency_pair = models.PositiveIntegerField(default=None, null=True)
    buy = models.PositiveIntegerField()
    spread = models.FloatField(help_text='発注決定時のスプレッド（発注時の値は取得できない）')
    open_rate = models.FloatField(default=None, null=True, help_text='想定注文レート')
    lowerBound = models.FloatField(default=None, null=True, help_text='成行注文時の最大下限レート')
    upperBound = models.FloatField(default=None, null=True, help_text='成行注文時の最大上限レート')
    real_open_rate = models.FloatField(default=None, null=True, help_text='約定時の注文レート')
    limit_rate = models.FloatField()
    stop_limit_rate = models.FloatField()
    real_limit_rate = models.FloatField(default=None, null=True, help_text='約定時の注文レート')
    real = models.PositiveIntegerField(default=0, db_index=True)
    profit = models.PositiveIntegerField(default=None, null=True)
    units = models.PositiveIntegerField(default=None, null=True, help_text='注文量')

    class Meta(object):
        app_label = 'board'

    @classmethod
    def pre_order(cls, ai_board, order, price, prev_rate_at):
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
            limit_rate = open_rate + float(order.limit * price.currency_pair.get_base_tick())
            stop_limit_rate = open_rate - float(order.stop_limit * price.currency_pair.get_base_tick())
        else:
            # sell
            open_rate = price.ask
            limit_rate = open_rate - float(order.limit * price.currency_pair.get_base_tick())
            stop_limit_rate = open_rate + float(order.stop_limit * price.currency_pair.get_base_tick())

        upperBound = open_rate + 3 * price.currency_pair.get_base_tick()
        lowerBound = open_rate - 3 * price.currency_pair.get_base_tick()

        # create
        return cls.objects.create(real=real,
                                  ai_board_id=ai_board_id,
                                  _currency_pair=currency_pair,
                                  buy=buy,
                                  spread=spread,
                                  open_rate=open_rate,
                                  limit_rate=limit_rate,
                                  stop_limit_rate=stop_limit_rate,
                                  prev_rate_at=prev_rate_at,
                                  lowerBound=lowerBound,
                                  upperBound=upperBound,
                                  units=ai_board.units)

    @property
    def currency_pair(self):
        return CurrencyPair(self._currency_pair)

    @property
    def side(self):
        return 'buy' if self.buy else 'sell'

    def set_order(self, orders_response):
        """
        確定した注文を記録
        """
        self.order_at = orders_response.time
        self.real_open_rate = orders_response.price
        self.oanda_ticket_id = orders_response.tradeOpened.oanda_ticket_id
        self.save()
        pass
