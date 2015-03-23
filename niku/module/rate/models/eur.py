# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from enum import Enum
import pytz
from .base import CurrencyCandleBase
from .test_data import TestDataMixin
from .moving_average import MovingAverageBase
from ..consts import Granularity, CurrencyPair


class EurUsdMA(MovingAverageBase):
    currency_pair = CurrencyPair.EUR_USD


class CandleEurUsdBase(TestDataMixin, CurrencyCandleBase):
    tick = 0.0001
    MA_CLS = EurUsdMA
    currency_pair = CurrencyPair.EUR_USD

    class Meta(object):
        app_label = 'rate'
        abstract = True
        unique_together = ('start_at',)


class CandleEurUsdM1Rate(CandleEurUsdBase):
    _granularity = Granularity.M1
    currency_pair = CurrencyPair.EUR_USD


class CandleEurUsdM5Rate(CandleEurUsdBase):
    _granularity = Granularity.M5
    currency_pair = CurrencyPair.EUR_USD


class CandleEurUsdH1Rate(CandleEurUsdBase):
    _granularity = Granularity.H1
    currency_pair = CurrencyPair.EUR_USD


class CandleEurUsdDRate(CandleEurUsdBase):
    _granularity = Granularity.D
    currency_pair = CurrencyPair.EUR_USD
