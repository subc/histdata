# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from __future__ import absolute_import
from __future__ import unicode_literals
import copy
from django.core.management import BaseCommand, CommandError
import numpy
import requests
from module.ai.models import AI2EurUsd
from module.genetic.models import GeneticHistory
from module.genetic.models.history import GeneticEliteHistory
from module.rate.models import CandleEurUsdM5Rate
from module.rate.models.base import MultiCandles
from module.rate.models.eur import Granularity, CandleEurUsdH1Rate, CandleEurUsdM1Rate
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
        set_candle_to_cache()
        elite_group = GeneticEliteHistory.objects.filter(progress=None)
        ai_group = []
        for history in [e.history for e in elite_group]:
            ai = AI2EurUsd.get_ai(history)
            H1, M5, M1 = calc(ai)
            history_elite_write(H1, M5, M1)

        print ai_group


def calc(ai):
    return benchmark(ai)


def benchmark(ai):
    aiH1 = None
    aiM5 = None
    aiM1 = None

    H1candles = cache.get('candlesH1')
    M5candles = cache.get('candlesM5')
    M1candles = cache.get('candlesH1')

    # 確定処理
    if H1candles:
        aiH1 = copy.deepcopy(ai)
        marketH1 = Market(aiH1.pk, calc_draw_down=True)
        aiH1 = loop(aiH1, H1candles, marketH1)
        rate = H1candles[-1]
        aiH1.update_market(marketH1, H1candles[-1])

    if M5candles:
        aiM5 = copy.deepcopy(ai)
        marketM5 = Market(aiM5.pk, calc_draw_down=True)
        aiM5 = loop(aiM5, M5candles, marketM5)
        rate = M5candles[-1]
        aiM5.update_market(marketM5, M5candles[-1])

    if M1candles:
        aiM1 = copy.deepcopy(ai)
        marketM1 = Market(aiM1.pk, calc_draw_down=True)
        aiM1 = loop(aiM1, M1candles, marketM1)
        rate = M1candles[-1]
        aiM1.update_market(marketM1, M1candles[-1])
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    if H1candles:
        print('[ID:{}]H1ただいまの利益:{}円 ポジション損益:{}円 ポジション数:{} 総取引回数:{}'.format(aiH1.pk,
                                                                         marketH1.profit_summary(rate),
                                                                         marketH1.current_profit(rate),
                                                                         len(marketH1.open_positions),
                                                                         len(marketH1.positions)))
        print('H1最大利益:{}円 最小利益:{}円'.format(marketH1.profit_max, marketH1.profit_min))
    if M5candles:
        print '++++++++++++++++'
        print('[ID:{}]M5ただいまの利益:{}円 ポジション損益:{}円 ポジション数:{} 総取引回数:{}'.format(aiM5.pk,
                                                                         marketM5.profit_summary(rate),
                                                                         marketM5.current_profit(rate),
                                                                         len(marketM5.open_positions),
                                                                         len(marketM5.positions)))
        print('M5最大利益:{}円 最小利益:{}円'.format(marketM5.profit_max, marketM5.profit_min))
    if M1candles:
        print '++++++++++++++++'
        print('[ID:{}][M1]ただいまの利益:{}円 ポジション損益:{}円 ポジション数:{} 総取引回数:{}'.format(aiM1.pk,
                                                                         marketM1.profit_summary(rate),
                                                                         marketM1.current_profit(rate),
                                                                         len(marketM1.open_positions),
                                                                         len(marketM1.positions)))
        print('[M1]最大利益:{}円 最小利益:{}円'.format(marketM1.profit_max, marketM1.profit_min))
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'


    return aiH1, aiM5, aiM1


def loop(ai, candles, market):
    prev_rates = []
    for rate in candles:
        # 購入判断(prev rateに未来データを投入しないこと！！)
        market = ai.order(market, prev_rates, rate.open_bid, rate.start_at)

        # 決済
        market.payment(rate)

        # 過去のレートを更新
        prev_rates.append(rate)

    return ai


def set_candle_to_cache():
    candles = CandleEurUsdH1Rate.get_test_data()
    cache.set('candlesH1', candles, timeout=720000)

    candles = CandleEurUsdM5Rate.get_test_data()
    cache.set('candlesM5', candles, timeout=720000)

    candles = CandleEurUsdM1Rate.get_test_data()
    cache.set('candlesM1', candles, timeout=720000)


def history_elite_write(H1, M5, M1):
    """
    HTTP通信で書き込む
    """
    url_base = 'http://{}/genetic/history/elite'
    payload = ujson.dumps({
        'genetic_id': H1.pk,
        'profitH1': H1.profit if H1 else 0,
        'profitH1_max': H1.profit_max if H1 else 0,
        'profitH1_min': H1.profit_min if H1 else 0,
        'profitM5': M5.profit if M5 else 0,
        'profitM5_max': M5.profit_max if M5 else 0,
        'profitM5_min': M5.profit_min if M5 else 0,
        'profitM1': M1.profit if M1 else 0,
        'profitM1_max': M1.profit_max if M1 else 0,
        'profitM1_min': M1.profit_min if M1 else 0,
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