# -*- coding: utf-8 -*-
"""
キャンドルクラスのテスト
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import random
from collections import defaultdict
from django.core.management import BaseCommand
from module.rate.models import CandleEurUsdH1Rate


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        objects = CandleEurUsdH1Rate.get_all()
        print 'キャンドル数:', len(objects)
        d = defaultdict(list)
        for o in objects:
            d[o.get_candle_type(20)].append(1)
        d2 = {}
        for key in d:
            d2[key] = len(d[key])
            print '{}:{}'.format(key, d2[key])
