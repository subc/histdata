# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from module.rate import CurrencyPair
from module.rate.models import CandleUsdJpyH1Rate, CandleEurUsdH1Rate, CandleGbpUsdH1Rate, CandleAudUsdH1Rate
from module.rate.models.eur import EurUsdMA
from module.rate.models.usd import UsdJpyMA
from module.rate.models.gbp import GbpUsdMA
from module.rate.models.aud import AudUsdMA


class CurrencyMixinBase(object):
    base_tick = None
    yen = None

    @classmethod
    def tick_to_yen(cls, tick):
        """
        :param tick: float
        :rtype : int
        """
        return int(float(tick / cls.base_tick) * cls.yen)


class EurUsdMixin(CurrencyMixinBase):
    CANDLE_CLS = CandleEurUsdH1Rate
    CANDLE_MA_CLS = EurUsdMA
    base_tick = 0.0001
    yen = 140  # 1tick幾らか
    currency_pair = CurrencyPair.EUR_USD


class UsdJpyMixin(CurrencyMixinBase):
    CANDLE_CLS = CandleUsdJpyH1Rate
    CANDLE_MA_CLS = UsdJpyMA
    base_tick = 0.01
    yen = 120  # 1tick幾らか
    currency_pair = CurrencyPair.USD_JPY


class UsdJMixin(CurrencyMixinBase):
    CANDLE_CLS = CandleUsdJpyH1Rate
    CANDLE_MA_CLS = UsdJpyMA
    base_tick = 0.01
    yen = 120  # 1tick幾らか
    currency_pair = CurrencyPair.USD_JPY


class GbpUsdMixin(CurrencyMixinBase):
    CANDLE_CLS = CandleGbpUsdH1Rate
    CANDLE_MA_CLS = GbpUsdMA
    base_tick = 0.0001
    yen = 180  # 1tick幾らか
    currency_pair = CurrencyPair.GBP_USD


class AudUsdMixin(CurrencyMixinBase):
    CANDLE_CLS = CandleAudUsdH1Rate
    CANDLE_MA_CLS = AudUsdMA
    base_tick = 0.0001
    yen = 94  # 1tick幾らか
    currency_pair = CurrencyPair.AUD_USD