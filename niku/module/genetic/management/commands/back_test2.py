# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
from module.genetic.models import Benchmark
from module.genetic.models.mixin import GeneticMixin, ApiMixin
from module.rate.models import CandleEurUsdH1Rate
from module.rate.models.eur import EurUsdMA
from module.ai.models import AI5EurUsd as AI

# 最初の世代数
AI_START_GENERATION = 1
AI_START_NUM = 2
AI_GROUP_SIZE = 20
GENERATION_LIMIT = 300


class Command(ApiMixin, GeneticMixin, BaseCommand):
    generation = AI_START_GENERATION

    def handle(self, *args, **options):
        self.run()

    def run(self):
        candles = get_candles()
        ai_group = get_ai_group(self.suffix, AI_START_NUM, self.generation)
        benchmark = Benchmark(candles)

        # 特定世代まで試験を実施
        while self.generation <= GENERATION_LIMIT:
            # ベンチマーク実行
            ai_group = benchmark.set_ai(ai_group).run_mp()
            score = max([ai.profit for ai in ai_group])
            self.history_write(ai_group)

            # 一定性能以下のAIグループは足切り絶滅
            self.ai_terminate(ai_group)

            # 選択と交叉
            ai_group = self.cross_over(AI_GROUP_SIZE, ai_group)

            # normalization
            for ai in ai_group:
                ai.normalization()

            print '第{}世代 完了![score:{}]'.format(self.generation, score)

    def ai_terminate(self, ai_group):
        """
        一定性能以下のAIグループは足切り絶滅
        """
        self.generation += 100000

    @property
    def suffix(self):
        """
        名前の接頭語を返却
        :rtype : string
        """
        return 'test-ai'

    @property
    def ai_class(self):
        return AI


def get_ai_group(suffix, num, generation):
    """
    :rtype : list of AI
    """
    base_ai = AI({}, suffix, generation)
    return base_ai.initial_create(num)


def get_candles():
    """
    :rtype : list of Rate
    """
    candles = CandleEurUsdH1Rate.get_test_data()
    ma = EurUsdMA.get_test_data()
    mad = {m.start_at: m for m in ma}
    for candle in candles:
        candle.set_ma(mad.get(candle.start_at))
    return candles