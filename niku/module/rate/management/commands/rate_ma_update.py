# -*- coding: utf-8 -*-
"""
MAを更新する
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import copy
import datetime
from django.core.management import BaseCommand
import pytz
from module.rate import CurrencyPair, CurrencyPairToTable
from module.rate.models.eur import CandleEurUsdDRate, CandleEurUsdM5Rate, EurUsdMA
from module.rate.models.usd import CandleUsdJpyM5Rate, CandleUsdJpyDRate, UsdJpyMA


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        for pair in [CurrencyPair.EUR_USD, CurrencyPair.USD_JPY]:
            self.update_ma(pair)

    def update_ma(self, pair):
        long_long_ago = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=365 * 100)
        print 'START IS {}'.format(long_long_ago)
        ma_cls = CurrencyPairToTable.get_ma_table(pair)
        ma_cls.sync(long_long_ago, pair)
