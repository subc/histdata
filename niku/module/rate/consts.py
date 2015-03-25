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
    GBP_USD = 3
    AUD_USD = 4

    def units_to_yen(self, tick, units):
        """
        1ティックを利益に変換
        :param tick: int
        :param units: int
        :rtype : float
        """
        if self == CurrencyPair.EUR_USD:
            return float(tick * units * 1.2) / 100
        elif self == CurrencyPair.USD_JPY:
            return float(tick * units * 1) / 100
        raise ValueError

    def tick_to_yen(self, tick):
        """
        1通貨単位分の利益を円換算する
        AI専用
        """
        if self == CurrencyPair.EUR_USD:
            return int(tick * 10000 * 140)
        elif self == CurrencyPair.USD_JPY:
            return int(tick * 100 * 100)
        raise ValueError

    def get_base_tick(self):
        """
        :rtype: float
        """
        d = {
            CurrencyPair.EUR_USD: 0.0001,
            CurrencyPair.USD_JPY: 0.01,
            CurrencyPair.GBP_USD: 0.0001,
            CurrencyPair.AUD_USD: 0.0001,
        }
        return d.get(self)


class CurrencyPairToTable(object):
    @classmethod
    def get_table(cls, currency_pair, granularity):
        """
        :param currency_pair: CurrencyPair
        :param granularity: Granularity
        :rtype : CurrencyCandleBase
        """
        from .models import CandleEurUsdM1Rate, CandleEurUsdDRate, CandleEurUsdH1Rate, CandleEurUsdM5Rate
        from .models import CandleUsdJpyM1Rate, CandleUsdJpyDRate, CandleUsdJpyH1Rate, CandleUsdJpyM5Rate
        from .models import CandleAudUsdDRate, CandleAudUsdH1Rate, CandleAudUsdM1Rate, CandleAudUsdM5Rate
        from .models import CandleGbpUsdDRate, CandleGbpUsdH1Rate, CandleGbpUsdM1Rate, CandleGbpUsdM5Rate

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
            },
            CurrencyPair.AUD_USD: {
                Granularity.D: CandleAudUsdDRate,
                Granularity.H1: CandleAudUsdH1Rate,
                Granularity.M5: CandleAudUsdM5Rate,
                Granularity.M1: CandleAudUsdM1Rate,
            },
            CurrencyPair.GBP_USD: {
                Granularity.D: CandleGbpUsdDRate,
                Granularity.H1: CandleGbpUsdH1Rate,
                Granularity.M5: CandleGbpUsdM5Rate,
                Granularity.M1: CandleGbpUsdM1Rate,
            }
        }
        return CURRENCY_PAIR_TO_TABLE.get(currency_pair).get(granularity)

    @classmethod
    def get_ma_table(cls, currency_pair):
        """
        :param currency_pair: CurrencyPair
        :rtype : MovingAverageBase
        """
        from .models.eur import EurUsdMA
        from .models.usd import UsdJpyMA
        from .models.aud import AudUsdMA
        from .models.gbp import GbpUsdMA
        CURRENCY_PAIR_TO_TABLE = {
            CurrencyPair.EUR_USD: EurUsdMA,
            CurrencyPair.USD_JPY: UsdJpyMA,
            CurrencyPair.AUD_USD: AudUsdMA,
            CurrencyPair.GBP_USD: GbpUsdMA,
        }
        return CURRENCY_PAIR_TO_TABLE.get(currency_pair)
