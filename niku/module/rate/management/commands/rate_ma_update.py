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
import gc
from module.rate import CurrencyPair, CurrencyPairToTable, Granularity
from module.rate.models.eur import CandleEurUsdDRate, CandleEurUsdM5Rate, EurUsdMA
from module.rate.models.usd import CandleUsdJpyM5Rate, CandleUsdJpyDRate, UsdJpyMA


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        for pair in CurrencyPair:
            self.update_ma(pair)

    def update_ma(self, pair):
        ma_cls = CurrencyPairToTable.get_ma_table(pair)
        m5_cls = CurrencyPairToTable.get_table(pair, Granularity.M5)
        m5_all = m5_cls.by_start_at(datetime.datetime(year=2014, month=12, day=20, tzinfo=pytz.utc))

        # maテーブルをトランケート
        ma_cls.objects.all().delete()

        bulk = []
        ct = 0
        for candle in m5_all:
            bulk.append(ma_cls.create_from_candle(candle, pair))  # ma計算
            ct += 1
            if len(bulk) > 3000:
                print '{}/{}'.format(ct, len(m5_all))
                ma_cls.objects.bulk_create(bulk)  # bulk!
                del bulk  # メモリ解放
                bulk = []

        if bulk:
            m5_cls.objects.bulk_create(bulk)

        # メモリ解放
        gc.collect()