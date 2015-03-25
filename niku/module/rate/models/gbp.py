# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from .base import CurrencyCandleBase
from module.rate import Granularity, CurrencyPair
from module.rate.models.test_data import TestDataMixin
from .moving_average import MovingAverageBase


class GbpUsdMA(MovingAverageBase):
    currency_pair = CurrencyPair.GBP_USD


class CandleGbpUsdBase(TestDataMixin, CurrencyCandleBase):
    tick = 0.0001
    MA_CLS = GbpUsdMA
    currency_pair = CurrencyPair.GBP_USD

    class Meta(object):
        app_label = 'rate'
        abstract = True
        unique_together = ('start_at',)


class CandleGbpUsdM1Rate(CandleGbpUsdBase):
    _granularity = Granularity.M1
    currency_pair = CurrencyPair.GBP_USD


class CandleGbpUsdM5Rate(CandleGbpUsdBase):
    _granularity = Granularity.M5
    currency_pair = CurrencyPair.GBP_USD


class CandleGbpUsdH1Rate(CandleGbpUsdBase):
    _granularity = Granularity.H1
    currency_pair = CurrencyPair.GBP_USD


class CandleGbpUsdDRate(CandleGbpUsdBase):
    _granularity = Granularity.D
    currency_pair = CurrencyPair.GBP_USD
