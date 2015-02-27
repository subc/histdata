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
        }
        return GranularityToDBTable.get(self)


class CandleEurUsdBase(CurrencyCandleBase):
    tick = 0.0001

    class Meta(object):
        app_label = 'rate'
        abstract = True
        unique_together = ('start_at',)


class CandleEurUsdM5Rate(CandleEurUsdBase):
    _granularity = Granularity.M5


class CandleEurUsdH1Rate(CandleEurUsdBase):
    _granularity = Granularity.H1
    CACHE_TEST_DATA2 = None

    @classmethod
    def get_test_data(cls):
        return cls.sort(list(cls.objects.filter(id__lte=5001)))

    @classmethod
    def get_test_data2(cls):
        if cls.CACHE_TEST_DATA2:
            return cls.CACHE_TEST_DATA2

        r = cls.sort(list(cls.objects.filter(start_at__gte=datetime.datetime(2010, 1, 1, tzinfo=pytz.utc))))
        cls.CACHE_TEST_DATA2 = r
        return r


class CandleEurUsdDRate(CandleEurUsdBase):
    _granularity = Granularity.D