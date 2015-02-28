# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import random
from enum import Enum


class OrderType(Enum):
    BUY = 1
    WAIT = 0
    SELL = -1

    @classmethod
    def cross_over(cls, value_a, value_b):
        if not (type(value_a) == type(value_b) == cls):
            raise TypeError
        return value_b, value_a

    @classmethod
    def mutation(cls, value):
        """
        突然変異
        異なる値になる
        :param value: OrderType
        :rtype : OrderType
        """
        _all = list(cls)
        random.shuffle(_all)
        for _a in _all:
            if value != _a:
                return value
        raise ValueError

    def order_reverse(self):
        """
        注文方向を反転させる
        :rtype : OrderType
        """
        return OrderType(-1 * self.value)