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

    def __init__(self, rate, order_ai):
        """
        :param rate: Rate
        :param order_ai: OrderAI
        """
        if order_ai.order_type == OrderType.WAIT:
            return
        self.open_bid = rate.open_bid

        is_buy = True if order_ai.order_type == OrderType.BUY else False
        if is_buy:
            self.limit_bid = rate.open_bid + rate.tick * order_ai.limit
            self.stop_limit_bid = rate.open_bid - rate.tick * order_ai.stop_limit
        else:
            self.limit_bid = rate.open_bid - rate.tick * order_ai.limit
            self.stop_limit_bid = rate.open_bid + rate.tick * order_ai.stop_limit


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