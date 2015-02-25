# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from enum import Enum
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


class CandleEurUsdDRate(CandleEurUsdBase):
    _granularity = Granularity.D