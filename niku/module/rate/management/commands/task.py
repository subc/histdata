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
        # copy elite
        self.copy_elite()

        # back_test
        self.back_test()

        # 10秒止まる
        time.sleep(10)

    def copy_elite(self):
        CopyEliteCmd().run()

    def back_test(self):
        BackTestCmd().run()