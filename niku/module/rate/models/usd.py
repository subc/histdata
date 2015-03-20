# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from .base import CurrencyCandleBase
from module.rate import Granularity, CurrencyPair
from module.rate.models.test_data import TestDataMixin
from .moving_average import MovingAverageBase


class UsdJpyMA(MovingAverageBase):
    currency_pair = CurrencyPair.USD_JPY


class CandleUsdJpyBase(TestDataMixin, CurrencyCandleBase):
    MA_CLS = UsdJpyMA
    currency_pair = CurrencyPair.USD_JPY

    class Meta(object):
        app_label = 'rate'
        abstract = True
        unique_together = ('start_at',)

    @property
    def tick(self):
        return self.currency_pair.get_base_tick()


class CandleUsdJpyM1Rate(CandleUsdJpyBase):
    _granularity = Granularity.M1
    currency_pair = CurrencyPair.USD_JPY


class CandleUsdJpyM5Rate(CandleUsdJpyBase):
    _granularity = Granularity.M5
    currency_pair = CurrencyPair.USD_JPY


class CandleUsdJpyH1Rate(CandleUsdJpyBase):
    _granularity = Granularity.H1
    currency_pair = CurrencyPair.USD_JPY


class CandleUsdJpyDRate(CandleUsdJpyBase):
    _granularity = Granularity.D
    currency_pair = CurrencyPair.USD_JPY
