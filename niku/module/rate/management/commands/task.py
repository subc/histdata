# -*- coding: utf-8 -*-
"""
複合タスクを実行する
01. レートの更新
02. MAの更新
03. copy elite
04. back_test
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import copy
import datetime
from django.core.management import BaseCommand
import pytz
from module.rate import CurrencyPair, Granularity
from module.rate.models.eur import CandleEurUsdDRate, CandleEurUsdM5Rate, EurUsdMA
from module.rate.models.usd import CandleUsdJpyM5Rate, CandleUsdJpyDRate, UsdJpyMA
from .rate_update import Command as RateUpdateCmd
from .rate_ma_update import Command as RateMaUpdateCmd
from module.genetic.management.commands.copy_elite import Command as CopyEliteCmd
from module.genetic.management.commands.back_test import Command as BackTestCmd
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        # 01. レートの更新
        # self.rate_update()

        # 02. MAの更新
        # self.ma_update()

        # 03. copy elite
        self.copy_elite()

        # 04. back_test
        self.back_test()

        # 10秒止まる
        time.sleep(10)

    def rate_update(self):
        # 01. レートの更新
        now = datetime.datetime.now(pytz.utc)
        two_days_ago = now - datetime.timedelta(seconds=3600*24*7)
        cmd = RateUpdateCmd()
        for pair in CurrencyPair:
            cmd.update_rate(pair, Granularity.D, 700, limit=two_days_ago)
            cmd.update_rate(pair, Granularity.H1, 100, limit=two_days_ago)
            cmd.update_rate(pair, Granularity.M5, 15, limit=two_days_ago)
            cmd.update_rate(pair, Granularity.M1, 2, limit=two_days_ago)

    def ma_update(self):
        # 02. MAの更新
        cmd = RateMaUpdateCmd()
        now = datetime.datetime.now(pytz.utc)
        thirty_days_ago = now - datetime.timedelta(seconds=3600*24*30)
        seven_days_ago = now - datetime.timedelta(seconds=3600*24*7)

        # EUR_USD
        write_history = [x.start_at for x in EurUsdMA.by_start_at(thirty_days_ago)]
        candles_m5 = CandleEurUsdM5Rate.by_start_at(seven_days_ago)
        candles_d1 = CandleEurUsdDRate.by_start_at(seven_days_ago)
        cmd.write(EurUsdMA, write_history, candles_m5, candles_d1)

        # EUR_USD
        write_history = [x.start_at for x in UsdJpyMA.by_start_at(thirty_days_ago)]
        candles_m5 = CandleUsdJpyM5Rate.by_start_at(seven_days_ago)
        candles_d1 = CandleUsdJpyDRate.by_start_at(seven_days_ago)
        cmd.write(UsdJpyMA, write_history, candles_m5, candles_d1)

    def copy_elite(self):
        CopyEliteCmd().run()

    def back_test(self):
        BackTestCmd().run()