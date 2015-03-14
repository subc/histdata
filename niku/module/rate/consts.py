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

    def db_table_class(self, currency_pair):
        """
        :param currency_pair: CurrencyPair
        :rtype : CurrencyCandleBase
        """
        return CurrencyPairToTable.get_table(currency_pair, self)


class CurrencyPair(Enum):
    EUR_USD = 1
    USD_JPY = 2

    def tick_to_yen(self, tick):
        """
        1通貨単位分の利益を円換算する
        """
        if self == CurrencyPair.EUR_USD:
            return int(tick * 10000 * 140)
        elif self == CurrencyPair.USD_JPY:
            return int(tick * 100 * 100)
        raise ValueError


class CurrencyPairToTable(object):
    @classmethod
    def get_table(cls, currency_pair, granularity):
        """
        :param currency_pair: CurrencyPair
        :param granularity: Granularity
        :rtype : CurrencyCandleBase
        """
        from .models.eur import CandleEurUsdM1Rate, CandleEurUsdDRate, CandleEurUsdH1Rate, CandleEurUsdM5Rate
        from .models.usd import CandleUsdJpyM1Rate, CandleUsdJpyDRate, CandleUsdJpyH1Rate, CandleUsdJpyM5Rate
        CURRENCY_PAIR_TO_TABLE = {
            CurrencyPair.EUR_USD: {
                Granularity.D: CandleEurUsdDRate,
                Granularity.H1: CandleEurUsdH1Rate,
                Granularity.M5: CandleEurUsdM5Rate,
                Granularity.M1: CandleEurUsdM1Rate,
            },
            CurrencyPair.USD_JPY: {
                Granularity.D: CandleUsdJpyDRate,
                Granularity.H1: CandleUsdJpyH1Rate,
                Granularity.M5: CandleUsdJpyM5Rate,
                Granularity.M1: CandleUsdJpyM1Rate,
            }
        }
        return CURRENCY_PAIR_TO_TABLE.get(currency_pair).get(granularity)
