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
from module.ai import AI1001UsdJpy as AI
from module.ai import AI2001Gbp as AI
from module.ai import AIHoriUsdJpy1002 as AI
from .genetic_single import Command as CmdBase


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

    def set_candles(self):
        """
        :rtype : list of Rate
        """
        candles = self.ai_class.CANDLE_CLS.get_test_data4()
        self.CANDLES = candles
