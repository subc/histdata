# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from enum import Enum
import pytz
from .base import CurrencyCandleBase
from .test_data import TestDataMixin
from .moving_average import MovingAverageBase
from ..consts import Granularity


class EurUsdMA(MovingAverageBase):
    pass


class CandleEurUsdBase(TestDataMixin, CurrencyCandleBase):
    tick = 0.0001
    MA_CLS = EurUsdMA

    class Meta(object):
        app_label = 'rate'
        abstract = True
        unique_together = ('start_at',)


class CandleEurUsdM1Rate(CandleEurUsdBase):
    _granularity = Granularity.M1

    @classmethod
    def get_test_data(cls):
        return list(cls.objects.filter(start_at__gte=datetime.datetime(2014, 10, 1, tzinfo=pytz.utc)).order_by('start_at'))


class CandleEurUsdM5Rate(CandleEurUsdBase):
    _granularity = Granularity.M5


class CandleEurUsdH1Rate(CandleEurUsdBase):
    _granularity = Granularity.H1


class CandleEurUsdDRate(CandleEurUsdBase):
    _granularity = Granularity.D
