# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from module.genetic.models.parameter import OrderType


class MarketOrder(object):
    """
    発注用クラス
    """
    order_type = None
    open_bid = None
    limit_bid = None
    stop_limit_bid = None

    def __init__(self, open_bid, base_tick, order_ai):
        """
        :param open_bid: float
        :param base_tick: float
        :param order_ai: OrderAI
        """
        self.order_type = order_ai.order_type
        if order_ai.order_type == OrderType.WAIT:
            return
        self.open_bid = open_bid

        is_buy = True if order_ai.order_type == OrderType.BUY else False
        if is_buy:
            self.limit_bid = open_bid + base_tick * order_ai.limit
            self.stop_limit_bid = open_bid - base_tick * order_ai.stop_limit
        else:
            self.limit_bid = open_bid - base_tick * order_ai.limit
            self.stop_limit_bid = open_bid + base_tick * order_ai.stop_limit

    @property
    def is_wait(self):
        return self.order_type == OrderType.WAIT

    @property
    def is_buy(self):
        return self.order_type == OrderType.BUY


class OrderAI(object):
    order_type = None
    limit = None
    stop_limit = None

    def __init__(self, order_type, limit, stop_limit):
        """
        :param order_type: OrderType
        :param limit: int
        :param stop_limit: int
        """
        assert type(order_type) == OrderType
        self.order_type = order_type
        self.limit = limit
        self.stop_limit = stop_limit