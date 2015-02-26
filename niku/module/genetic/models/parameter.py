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

        # Not Wait
        if value_a != cls.WAIT and value_a != cls.WAIT:
            # aとbが同じときはreturn a, a と return b, aが等価なのでこれ問題ない
            return value_b, value_a

        # Wait
        if value_a == value_b:
            return value_a, value_b
        if random.randint(1, 2) == 1:
            return value_b, value_a
        else:
            if random.randint(1, 2) == 1:
                return value_a, value_a
            else:
                return value_b, value_b