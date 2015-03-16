# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from enum import Enum
import pytz
from .base import CurrencyCandleBase
from module.rate import Granularity
from module.rate.models.test_data import TestDataMixin
from .moving_average import MovingAverageBase


class UsdJpyMA(MovingAverageBase):
    pass


class CandleUsdJpyBase(TestDataMixin, CurrencyCandleBase):
    tick = 0.0001
    MA_CLS = UsdJpyMA

    class Meta(object):
        app_label = 'rate'
        abstract = True
        unique_together = ('start_at',)


class CandleUsdJpyM1Rate(CandleUsdJpyBase):
    _granularity = Granularity.M1


class CandleUsdJpyM5Rate(CandleUsdJpyBase):
    _granularity = Granularity.M5


class CandleUsdJpyH1Rate(CandleUsdJpyBase):
    _granularity = Granularity.H1


class CandleUsdJpyDRate(CandleUsdJpyBase):
    _granularity = Granularity.D
