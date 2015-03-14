# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import numpy
from module.genetic.models.benchmark_single import BenchmarkSingle
from module.genetic.models.mixin import GeneticMixin, ApiMixin
from module.ai import AI10EurUsd as AI


class Command(ApiMixin, GeneticMixin, BaseCommand):
    # 最初の世代数
    AI_START_GENERATION = 1
    AI_START_NUM = 20
    AI_GROUP_SIZE = 20
    GENERATION_LIMIT = 300
    generation = AI_START_GENERATION
    CANDLES = None

    def handle(self, *args, **options):
        self.set_candles()
        while True:
            self.generation = self.AI_START_GENERATION
            self.run()

    def run(self):
        ai_group = get_ai_group(self.ai_class, self.suffix, self.AI_START_NUM, self.generation)
        benchmark = BenchmarkSingle(self.CANDLES)

        # 特定世代まで試験を実施
        while self.generation <= self.GENERATION_LIMIT:
            # ベンチマーク実行
            ai_group = benchmark.set_ai(ai_group).run()
            score = max([ai.score(0) for ai in ai_group])
            profit = max([ai.profit for ai in ai_group])
            self.history_write(ai_group)

            # 一定性能以下のAIグループは足切り絶滅
            self.generation += 1
            self.ai_terminate(ai_group, profit)

            # 選択と交叉
            ai_group = self.cross_over(self.AI_GROUP_SIZE, ai_group)

            # normalization
            for ai in ai_group:
                ai.normalization()
            print '第{}世代 完了![score:{}] profit:{}'.format(self.generation, score, profit)

    def ai_terminate(self, ai_group, score):
        """
        一定性能以下のAIグループは足切り絶滅
        """
        # 取引数による詰み回避
        trade_count = numpy.average([len(ai.market.positions) for ai in ai_group])
        if trade_count < 1000:
            print "取引平均回数が1000を下回ったので自殺:count:{}".format(trade_count)
            self.generation += 100000

        # 利益による詰み回避
        g = self.generation
        if g >= 10 and score < 0:
            self.generation += 100000
        if g >= 20 and score < 100 * 10000:
            self.generation += 100000
        if g >= 40 and score < 180 * 10000:
            self.generation += 100000
        if g >= 60 and score < 200 * 10000:
            self.generation += 100000
        if g >= 100 and score < 250 * 10000:
            self.generation += 100000

    @property
    def suffix(self):
        """
        名前の接頭語を返却
        :rtype : string
        """
        return 'S-'

    @property
    def ai_class(self):
        return AI

    def set_candles(self):
        """
        :rtype : list of Rate
        """
        candles = AI.CANDLE_CLS.get_test_data()
        ma = AI.CANDLE_MA_CLS.get_test_data()
        mad = {m.start_at: m for m in ma}
        for candle in candles:
            candle.set_ma(mad.get(candle.start_at))
        self.CANDLES = candles


def get_ai_group(ai_class, suffix, num, generation):
    """
    :rtype : list of AI
    """
    base_ai = ai_class({}, suffix, generation)
    return base_ai.initial_create(num)
