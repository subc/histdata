# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import numpy
from module.genetic.models import Benchmark
from module.genetic.models.mixin import GeneticMixin, ApiMixin
from module.rate.models import CandleEurUsdH1Rate
from module.rate.models.eur import EurUsdMA
from module.ai import AI9EurUsd as AI
from .genetic import Command as CmdBase


class Command(CmdBase):
    # 最初の世代数
    AI_START_GENERATION = 1
    AI_START_NUM = 20
    AI_GROUP_SIZE = 20
    GENERATION_LIMIT = 10
    IS_SINGLE = True

    def ai_terminate(self, ai_group, score):
        pass

    @property
    def suffix(self):
        """
        名前の接頭語を返却
        :rtype : string
        """
        return 'TEST'

    @property
    def ai_class(self):
        return AI

    def get_candles(self):
        """
        :rtype : list of Rate
        """
        candles = CandleEurUsdH1Rate.get_test_data4()
        ma = EurUsdMA.get_test_data4()
        mad = {m.start_at: m for m in ma}
        for candle in candles:
            candle.set_ma(mad.get(candle.start_at))
        return candles