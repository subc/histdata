# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from .base import CurrencyCandleBase
from module.rate import Granularity, CurrencyPair
from module.rate.models.test_data import TestDataMixin
from .moving_average import MovingAverageBase


class AudUsdMA(MovingAverageBase):
    currency_pair = CurrencyPair.AUD_USD


class CandleAudUsdBase(TestDataMixin, CurrencyCandleBase):
    tick = 0.0001
    MA_CLS = AudUsdMA
    currency_pair = CurrencyPair.AUD_USD

    class Meta(object):
        app_label = 'rate'
        abstract = True
        unique_together = ('start_at',)


class CandleAudUsdM1Rate(CandleAudUsdBase):
    _granularity = Granularity.M1
    currency_pair = CurrencyPair.AUD_USD


class CandleAudUsdM5Rate(CandleAudUsdBase):
    _granularity = Granularity.M5
    currency_pair = CurrencyPair.AUD_USD


class CandleAudUsdH1Rate(CandleAudUsdBase):
    _granularity = Granularity.H1
    currency_pair = CurrencyPair.AUD_USD


class CandleAudUsdDRate(CandleAudUsdBase):
    _granularity = Granularity.D
    currency_pair = CurrencyPair.AUD_USD
