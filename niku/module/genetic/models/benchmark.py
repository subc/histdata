# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.cache import cache
from utils.timeit import timeit
import multiprocessing
from module.market import Market

CACHE_CANDLES = 'CACHE_CANDLES'


class Benchmark(object):
    """
    AIのベンチマークを実施する。
    """
    PROCESS = 3
    _pool = None
    ai_group = None

    def __init__(self, candles):
        self.set_candles(candles)

    def set_ai(self, ai_group):
        self.ai_group = ai_group
        return self

    def set_candles(self, candles):
        """
        :param candles: list of Rate
        """
        cache.set(CACHE_CANDLES, candles, timeout=720000)
        return self

    def run(self, calc_draw_down=False):
        """
        ベンチマーク実行
        :rtype : list of AI
        """
        return [benchmark(ai, calc_draw_down=calc_draw_down) for ai in self.ai_group]

    def run_mp(self):
        """
        ベンチマークをマルチプロセスで実行する
        :rtype : list of AI
        """
        pool = multiprocessing.Pool(self.PROCESS)
        ai_group = pool.map(benchmark, self.ai_group)
        pool.close()  # マルチプロセス停止
        return ai_group


@timeit
def benchmark(ai, calc_draw_down=False):
    """
    :param ai: AI
    :param calc_draw_down: bool
    """
    print "START BENCHMARK"
    candles = cache.get(CACHE_CANDLES)
    market = Market(ai.generation, calc_draw_down=calc_draw_down)
    loop(ai, candles, market)

    # 確定処理
    # print "candles:{},{}".format(candles, len(candles))
    rate = candles[-1]
    ai.update_market(market, rate)
    print('[ID:{}]SCORE:{} PROFIT:{} OPEN-PROFIT:{} ポジション数:{} TRADE-COUNT:{}'.format(ai.generation,
                                                                          ai.score(0),
                                                                          market.profit_summary(rate),
                                                                          market.current_profit(rate),
                                                                          len(market.open_positions),
                                                                          len(market.positions)))
    print('SCORE-MAX:{} SCORE-MIN:{}'.format(market.profit_max, market.profit_min))
    print('AI KEYS:{}   [{}個超えたら危険]'.format(len(ai.ai_dict), len(market.positions) / 20))
    return ai


def loop(ai, candles, market):
    prev_rates = []
    for rate in candles:
        # 購入判断(prev rateに未来データを投入しないこと！！)
        market = ai.order(market, prev_rates, rate.open_bid, rate.start_at)

        # 決済
        market.payment(rate)

        # 過去のレートを更新
        prev_rates.append(rate)