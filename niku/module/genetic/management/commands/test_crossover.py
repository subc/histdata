# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand, CommandError
import requests
from module.genetic.models import GeneticHistory
from module.rate.models import CandleEurUsdM5Rate
from module.rate.models.eur import Granularity, CandleEurUsdH1Rate
from module.title.models.title import TitleSettings
from module.oanda.models.candle import OandaCandle
from utils import get_password
from utils.timeit import timeit
from utils.oanda_api import OandaAPI, Streamer
import ujson
import pytz
import requests
import random

MODE = {
    'sandbox': 'api-sandbox.oanda.com',
    'production': 'api-fxtrade.oanda.com',
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'STATUS'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

        for x in xrange(100):
            a = random.randint(5, 60)
            b = random.randint(5, 60)
            _a, _b = self.cross_2point(a, b)
            print '[{},{}] >> [{},{}]'.format(a, b, _a, _b)
        return a, b

    def cross_2point(self, a, b):
        """
        2点交叉
        :param a: int
        :param b: int
        """
        a = format(a, 'b')
        b = format(b, 'b')
        max_length = max([len(a), len(b)])
        if len(a) < max_length:
            a = '0' * (max_length - len(a)) + a
        if len(b) < max_length:
            b = '0' * (max_length - len(b)) + b

        point1 = random.randint(1, max_length)
        point2 = random.randint(1, max_length)
        print max_length, point1, point2
        point_max = max(point1, point2)
        point_min = min(point1, point2)

        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print '2点交叉スタート'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'base:{} , {}'.format(a, b)
        print '交叉点:{} , {}'.format(point_min, point_max)
        print a[:point_min] + b[point_min:point_max] + a[point_max:]
        print 'a[:point_min]', a[:point_min]
        print 'b[point_min:point_max]', b[point_min:point_max]
        print 'a[point_max:]', a[point_max:]
        print 'Bの場合'
        print b[:point_min] + a[point_min:point_max] + b[point_max:]
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        a = a[:point_min] + b[point_min:point_max] + a[point_max:]
        b = b[:point_min] + a[point_min:point_max] + b[point_max:]
        return int(a, 2), int(b, 2)