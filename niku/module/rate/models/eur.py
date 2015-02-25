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
            Granularity.D: CandleEurUsdM5Rate,
            Granularity.H1: CandleEurUsdH1Rate,
            Granularity.M5: CandleEurUsdDRate,
        }
        return GranularityToDBTable.get(self)


class CandleEurUsdM5Rate(CurrencyCandleBase):
    _granularity = Granularity.M5


class CandleEurUsdH1Rate(CurrencyCandleBase):
    _granularity = Granularity.H1


class CandleEurUsdDRate(CurrencyCandleBase):
    _granularity = Granularity.D

