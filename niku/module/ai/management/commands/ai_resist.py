# -*- coding: utf-8 -*-
"""
AIの変化耐性を調査する
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import copy
from django.core.management import BaseCommand, CommandError
import numpy
import requests
from module.ai.models import AI2EurUsd
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
from django.core.cache import cache
from module.genetic.management.commands.genetic_case1 import Market
import multiprocessing as mp


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        # 計算元データを計算
        candles = CandleEurUsdH1Rate.get_test_data2()
        cache.set('candles', candles, timeout=720000)

        ai_id = 27907  # 500世代
        ai_id = 25892  # 435
        # ai_id = 24348  # 358
        ai_id = 22652  # 273
        # ai_id = 20424  # 162
        # ai_id = 18074  # 40世代
        base_ai = AI2EurUsd.get_ai(GeneticHistory.get(ai_id))
        history_list = list(GeneticHistory.objects.filter(id__gte=17189,
                                                          id__lte=28079,
                                                          profit__gte=10700000))
        # print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        random.shuffle(history_list)
        for history in history_list:
            ai = AI2EurUsd.get_ai(history)
            score, draw_down_score = get_resist_point(ai)
            print "SCORE:%010d DRAW DOWN:%s" % (score, draw_down_score) +\
                  "第{}世代AI[id:{}]".format(ai.generation, ai.pk)


def get_resist_point(ai):
    """
    変化耐性を調査する
    :param ai: AI
    :rtype : score
    """
    def c(_ai):
        return copy.deepcopy(_ai)

    ai_group = [
        c(ai).incr_depth(x)
        for x in xrange(1, 24)
    ]
    ai_group += [
        c(ai).incr_base_tick(x)
        for x in xrange(-5, 5)
    ]
    # ai_group += [
    #     c(ai).mutation()
    #     for x in xrange(1, 50)
    # ]
    return calc(ai_group)


def calc(ai_group):
    # 初期AI集団生成
    generation = 1
    proc = 6  # 並列処理数 コア数以上にしても無駄
    # print ai_group
    # benchmark(ai_group[0])
    # raise

    pool = mp.Pool(proc)
    ai_group = ai_group
    ai_group = pool.map(benchmark, ai_group)
    score = numpy.average([ai.profit for ai in ai_group])
    draw_down_score = numpy.average([ai.market.profit_min for ai in ai_group])

    # pool内のワーカープロセスを停止する
    pool.close()
    return score, draw_down_score


def benchmark(ai):
    candles = cache.get('candles')
    market = Market(ai.pk, calc_draw_down=True)

    loop(ai, candles, market)

    # 確定処理
    rate = candles[-1]
    ai.update_market(market, rate)
    # print('[ID:{}]ただいまの利益:{}円 ポジション損益:{}円 ポジション数:{} 総取引回数:{}'.format(ai.pk,
    #                                                               market.profit_summary(rate),
    #                                                               market.current_profit(rate),
    #                                                               len(market.open_positions),
    #                                                               len(market.positions)))
    # print('最大利益:{}円 最小利益:{}円'.format(market.profit_max, market.profit_min))
    return ai


def loop(ai, candles, market):
    rates = []
    for rate in candles:
        rates.append(rate)

        # 購入判断
        market = ai.order(market, rates)

        # 決済
        market.payment(rate)
