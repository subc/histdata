# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from .models.eur import Granularity, CandleEurUsdM1Rate, CandleEurUsdDRate, CandleEurUsdH1Rate, CandleEurUsdM5Rate
from .models.currency_pair import CurrencyPair


CURRENCY_PAIR_TO_TABLE = {
    CurrencyPair.EUR_USD: {
        Granularity.D: CandleEurUsdDRate,
        Granularity.H1: CandleEurUsdH1Rate,
        Granularity.M5: CandleEurUsdM5Rate,
        Granularity.M1: CandleEurUsdM1Rate,

    },
    CurrencyPair.USD_JPY: {}
}

