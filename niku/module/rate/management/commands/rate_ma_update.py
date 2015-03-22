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
from module.rate import CurrencyPair, CurrencyPairToTable, Granularity
from module.rate.models.eur import CandleEurUsdDRate, CandleEurUsdM5Rate, EurUsdMA
from module.rate.models.usd import CandleUsdJpyM5Rate, CandleUsdJpyDRate, UsdJpyMA


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        for pair in [CurrencyPair.USD_JPY, CurrencyPair.GBP_USD, CurrencyPair.AUD_USD]:
            self.update_ma(pair)

    def update_ma(self, pair):
        long_long_ago = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=365 * 100)
        print 'START IS {}'.format(long_long_ago)
        ma_cls = CurrencyPairToTable.get_ma_table(pair)
        m5_cls = CurrencyPairToTable.get_table(pair, Granularity.M5)
        m5_all = m5_cls.get_all()

        # maテーブルをトランケート
        ma_cls.objects.all().delete()

        bulk = []
        ct = 0
        for candle in m5_all:
            bulk.append(ma_cls.create_from_candle(candle, pair))
            ct += 1
            if len(bulk) > 3000:
                print '{}/{}'.format(ct, len(m5_all))
                m5_cls.objects.bulk_create(bulk)

        if bulk:
            m5_cls.objects.bulk_create(bulk)