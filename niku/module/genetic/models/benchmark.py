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
    PROCESS = 8
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

    def run(self):
        """
        ベンチマーク実行
        :rtype : list of AI
        """
        return [benchmark(ai) for ai in self.ai_group]

    def run_mp(self):
        """
        ベンチマークをマルチプロセスで実行する
        :rtype : list of AI
        """
        ai_group = self.pool.map(benchmark, self.ai_group)
        self.pool.close()  # マルチプロセス停止
        return ai_group

    @property
    def pool(self):
        """
        マルチプロセスのpoolを返却
        """
        if self._pool:
            return self._pool
        self._pool = multiprocessing.Pool(self.PROCESS)
        return self._pool


@timeit
def benchmark(ai):
    """
    :param ai: AI
    """
    print "START BENCHMARK"
    candles = cache.get(CACHE_CANDLES)
    market = Market(ai.generation)
    loop(ai, candles, market)

    # 確定処理
    rate = candles[-1]
    ai.update_market(market, rate)
    print('[ID:{}]SCORE:{} OPEN-SCORE:{} ポジション数:{} TRADE-COUNT:{}'.format(ai.generation,
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