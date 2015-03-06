# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
from module.genetic.models.mixin import GeneticMixin, ApiMixin
from module.rate.models import CandleEurUsdH1Rate
from module.rate.models.eur import EurUsdMA


class Command(ApiMixin, GeneticMixin, BaseCommand):

    def handle(self, *args, **options):
        candles = get_candles()
        self.run(candles)

    def run(self, candles):
        d = {True: 0, False: 0}
        for candle in candles:
            if candle.ma:
                # print candle.start_at, candle.open_bid, candle.ma.d25
                # print candle.start_at, bool(candle.open_bid < candle.ma.d5)
                key = candle.open_bid < candle.ma.h24
                d[key] += 1
        print d


def get_candles():
    """
    :rtype : list of Rate
    """
    candles = CandleEurUsdH1Rate.get_test_data()
    ma = EurUsdMA.get_test_data()
    mad = {m.start_at: m for m in ma}
    for candle in candles:
        candle.set_ma(mad.get(candle.start_at))
    return candles