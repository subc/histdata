# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from __future__ import absolute_import
from __future__ import unicode_literals
import copy
from django.core.management import BaseCommand, CommandError
from line_profiler import LineProfiler
import numpy
import requests
from module.ai.models import AI2EurUsd
from module.rate import CurrencyPair, Granularity
from module.genetic.models import GeneticHistory, GeneticBackTestHistory
from module.genetic.models.back_test import get_candle_cls
from module.rate.models import CandleEurUsdM5Rate
from module.rate.models.base import MultiCandles
from module.rate.models.eur import CandleEurUsdH1Rate, CandleEurUsdM1Rate, EurUsdMA
from module.title.models.title import TitleSettings
from module.oanda.models.candle import OandaCandle
from utils import get_password
from utils.timeit import timeit
from utils.oanda_api import OandaAPI, Streamer
import ujson
import pytz
import requests
import random
import random
from django.core.cache import cache
from module.genetic.management.commands.genetic_case1 import Market
import multiprocessing as mp


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        for history in GeneticBackTestHistory.get_active():
            # AI LOAD
            ai = history.ai
            print '~~~~~~~~~~~~~~~~~~~~~~~'
            print '[AI:{} GENETIC:{}]START-AT:{}'.format(ai.ai_id, history.genetic_id, history.test_start_at)

            # CANDLES
            candles = list(history.candle_cls.by_start_at(history.test_start_at))
            ma = EurUsdMA.by_start_at(history.test_start_at)
            mad = {m.start_at: m for m in ma}
            for candle in candles:
                candle.set_ma(mad.get(candle.start_at))

            ai = benchmark(ai, candles)
            ai.genetic_history_id = history.id
            history_back_test_write([ai])


def benchmark(ai, candles):
    market = Market(ai.pk, calc_draw_down=True)
    ai = loop(ai, candles, market)
    rate = candles[-1]
    ai.update_market(market, candles[-1])

    # 取引回数がゼロのときはエラーで落とす
    if len(market.positions) == 0:
        raise ValueError, 'TRADE-COUNT IS ZERO'

    print('[ID:{}]SCORE:{} OPEN-SCORE:{} ポジション数:{} TRADE-COUNT:{}'.format(ai.generation,
                                                                          market.profit_summary(rate),
                                                                          market.current_profit(rate),
                                                                          len(market.open_positions),
                                                                          len(market.positions)))
    print('SCORE-MAX:{} SCORE-MIN:{}'.format(market.profit_max, market.profit_min))

    return ai


def loop(ai, candles, market):
    prev_rates = []
    ct = 0
    for rate in candles:
        # 購入判断(prev rateに未来データを投入しないこと！！)
        market = ai.order(market, prev_rates, rate.open_bid, rate.start_at)

        # 決済
        market.payment(rate)

        # 過去のレートを更新
        prev_rates.append(rate)

        if ct % 5000 == 0:
            print ct, '/', len(candles)
        ct += 1
    return ai


def set_candle_to_cache():
    print "start get candle H1"
    candles = CandleEurUsdH1Rate.get_test_data()
    cache.set('candlesH1', candles, timeout=720000)

    print "start get candle M5"
    candles = CandleEurUsdM5Rate.get_test_data()
    cache.set('candlesM5', candles, timeout=720000)

    print "start get candle M1"
    candles = CandleEurUsdM1Rate.get_test_data()
    cache.set('candlesM1', candles, timeout=720000)


def history_back_test_write(ai_group):
    """
    HTTP通信で書き込む
    """
    url_base = 'http://{}/genetic/history/back_test'
    payload = ujson.dumps({
        'ai_group': [ai.to_dict() for ai in ai_group],
    })
    response = requests_post_api(url_base, payload=payload)
    assert response.status_code == 200, response.text


def requests_post_api(url_base, payload=None):
    TEST_HOST = '127.0.0.1:8000'
    url = url_base.format(TEST_HOST)
    payload = {'data': payload}
    response = requests.post(url, data=payload)
    print 'URL SUCCESS: {}'.format(url)
    return response