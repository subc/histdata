# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from module.rate import CurrencyPair


class CurrencyMixinBase(object):
    base_tick = None
    yen = None

    @classmethod
    def tick_to_yen(cls, tick):
        """
        :param tick: float
        :rtype : int
        """
        return int(float(tick / cls.base_tick) * cls.yen)


class EurUsdMixin(CurrencyMixinBase):
    base_tick = 0.0001
    yen = 140  # 1tick幾らか
    currency_pair = CurrencyPair.EUR_USD