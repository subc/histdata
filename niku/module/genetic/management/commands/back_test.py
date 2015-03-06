# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
from module.genetic.models import Benchmark
from module.genetic.models.mixin import GeneticMixin, ApiMixin
from module.rate.models import CandleEurUsdH1Rate
from module.rate.models.eur import EurUsdMA
from module.ai.models import AI5EurUsd as AI
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
        for history in GeneticBackTestHistory.get_active():
            # AI LOAD
            ai = history.ai
            candles = get_candles(history)

            benchmark = Benchmark(candles)
            ai = benchmark.set_ai([ai]).run(calc_draw_down=True)[0]
            ai.genetic_history_id = history.id
            self.history_back_test_write([ai])


def get_candles(history):
    """
    :param history: GeneticBackTestHistory
    :rtype : list of Rate
    """
    candles = history.candle_cls.by_start_at(history.test_start_at)
    ma = EurUsdMA.by_start_at(history.test_start_at)
    mad = {m.start_at: m for m in ma}
    for candle in candles:
        candle.set_ma(mad.get(candle.start_at))
    return candles