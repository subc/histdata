# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from enum import Enum


class Granularity(Enum):
    D = 60 * 60 * 24
    H1 = 60 * 60
    M5 = 60 * 5
    M1 = 60
    UNKNOWN = 10000000000

    @property
    def db_table_class(self, currency_pair):
        """
        :param currency_pair: CurrencyPair
        :rtype : CurrencyCandleBase
        """
        return CurrencyPairToTable.get_table(currency_pair, self)


class CurrencyPair(Enum):
    EUR_USD = 1
    USD_JPY = 2


class CurrencyPairToTable(object):
    def get_table(self, currency_pair, granularity):
        from .models.eur import CandleEurUsdM1Rate, CandleEurUsdDRate, CandleEurUsdH1Rate, CandleEurUsdM5Rate
        CURRENCY_PAIR_TO_TABLE = {
            CurrencyPair.EUR_USD: {
                Granularity.D: CandleEurUsdDRate,
                Granularity.H1: CandleEurUsdH1Rate,
                Granularity.M5: CandleEurUsdM5Rate,
                Granularity.M1: CandleEurUsdM1Rate,

            },
            CurrencyPair.USD_JPY: {}
        }
        return CURRENCY_PAIR_TO_TABLE.get(currency_pair).get(granularity)
