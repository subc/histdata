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
        history_id = self._parse_args(args)
        self.run(history_id)

    def _parse_args(self, args):
        if len(args) != 1:
            raise CommandError(u'Usage: manage.py ai <ai_id>')
        history_id = int(args[0])

        return history_id

    def run(self, history_id):
        history = GeneticHistory.objects.get(id=history_id)
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'AI LOGIC'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        for key in sorted(history.ai, key=lambda x: x):
            print '{}:{}'.format(key, history.ai[key])
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'AI_KEYS:{}'.format(len(history.ai))

        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'MARKET'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print history.ai.get('MARKET')

        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'STATUS'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        # print '取引回数: {}'.format(len(history.ai.get('MARKET').get('positions')))


        # for x in CandleEurUsdH1Rate.get_test_data2():
        #     print x.start_at, x.open_bid, x.close_bid, x.high_bid, x.low_bid
        """
        ct:1 calc_rate:50
        ct:3 calc_rate:200
        ct:5 calc_rate:450
        ct:7 calc_rate:800
        ct:9 calc_rate:1250
        """

        ANS = {
            1000:5,
            500:4,
            360:4,
            270:3,
            120:2,
            50:0,
            30:0,
            0:0
        }

        ticks = [1000, 500, 360, 270, 120, 50, 49, 30, 0] + [0, -10, -49, -50, -51, -100, -120, -180, -270, -460]
        bp = 50
        for tick in ticks:
            print self.get_type(tick, bp), tick

        # for tick in ticks:
        #     result = 1
        #     prev_calc_rate = 0
        #     ct = 1
        #     for x in range(100):
        #         calc_rate = 50 * ct + prev_calc_rate
        #         print "ct:{} calc_rate:{}".format(ct, calc_rate)
        #         if calc_rate >= tick:
        #             print 'tick:{} result:{}'.format(tick, result)
        #             # assert ANS.get(tick) == result + 1
        #
        #             break
        #         ct += 2
        #         result += 1
        #         prev_calc_rate = calc_rate
        #

    def get_type(self, tick, base_tick):
        result = 1
        _tick = tick
        is_minus = False
        if tick < 0:
            _tick = tick * -1
            result = 0
            is_minus = True
        prev_calc_rate = 0
        ct = 1
        for x in range(10):
            calc_rate = base_tick * ct + prev_calc_rate
            if calc_rate >= _tick:
                return result
            ct += 2
            if is_minus:
                result -= 1
            else:
                result += 1
            prev_calc_rate = calc_rate
        raise ValueError
