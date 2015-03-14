# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from utils.timeit import timeit
from module.market import Market


class BenchmarkSingle(object):
    """
    AIのベンチマークを実施する。
    """
    ai_group = None
    CANDLES = None

    def __init__(self, candles):
        self.CANDLES = candles

    def set_ai(self, ai_group):
        self.ai_group = ai_group
        return self

    def run(self, calc_draw_down=False):
        """
        ベンチマーク実行
        :rtype : list of AI
        """
        return [self.benchmark(ai, calc_draw_down=calc_draw_down) for ai in self.ai_group]

    @timeit
    def benchmark(self, ai, calc_draw_down=False):
        """
        :param ai: AI
        :param calc_draw_down: bool
        """
        print "START BENCHMARK"
        market = Market(ai.generation, calc_draw_down=calc_draw_down)
        self.loop(ai, self.CANDLES, market)

        # 確定処理
        # print "candles:{},{}".format(candles, len(candles))
        rate = self.CANDLES[-1]
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

    def loop(self, ai, candles, market):
        prev_rates = []
        for rate in candles:
            # 購入判断(prev rateに未来データを投入しないこと！！)
            market = ai.order(market, prev_rates, rate.open_bid, rate.start_at)

            # 決済
            market.payment(rate)

            # 過去のレートを更新
            prev_rates.append(rate)