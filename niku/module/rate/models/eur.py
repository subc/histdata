# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from enum import Enum
import pytz
from .base import CurrencyCandleBase


class Granularity(Enum):
    D = 60 * 60 * 24
    H1 = 60 * 60
    M5 = 60 * 5
    M1 = 60
    UNKNOWN = 10000000000

    @property
    def db_table_class(self):
        """
        :rtype : CurrencyCandleBase
        """
        return self.get_database_table_class()

    def get_database_table_class(self):
        """
        :rtype : CurrencyCandleBase
        """
        GranularityToDBTable = {
            Granularity.D: CandleEurUsdDRate,
            Granularity.H1: CandleEurUsdH1Rate,
            Granularity.M5: CandleEurUsdM5Rate,
            Granularity.M1: CandleEurUsdM1Rate,
        }
        return GranularityToDBTable.get(self)


class CandleEurUsdBase(CurrencyCandleBase):
    tick = 0.0001

    class Meta(object):
        app_label = 'rate'
        abstract = True
        unique_together = ('start_at',)

    @classmethod
    def get_test_data(cls):
        return list(cls.objects.filter(start_at__gte=datetime.datetime(2010, 1, 1, tzinfo=pytz.utc)).order_by('start_at'))


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