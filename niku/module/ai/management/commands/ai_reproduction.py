# -*- coding: utf-8 -*-
"""
AI同士の遺伝子の近似度を調査する
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand, CommandError
import requests
from module.ai.models import AI2EurUsd
from module.genetic.models import GeneticHistory
from module.rate.models import CandleEurUsdM5Rate
from module.rate.models.eur import Granularity, CandleEurUsdH1Rate
from module.title.models.title import TitleSettings
from module.oanda.models.candle import OandaCandle
from utils import get_password
from utils.timeit import timeit
from utils.oanda_api import OandaAPI, Streamer
import ujson
import pytz
import requests
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        ai_id = self._parse_args(args)
        self.run(ai_id)

    def _parse_args(self, args):
        if len(args) != 1:
            raise CommandError(u'Usage: manage.py ai_reproduction <ai_id>')
        ai_id = int(args[0])

        return ai_id

    def run(self, ai_id):
        ai_id = 27907  # 500世代
        ai_id = 25892  # 435
        # ai_id = 24348  # 358
        ai_id = 22652  # 273
        # ai_id = 20424  # 162
        # ai_id = 18074  # 40世代
        base_ai = AI2EurUsd.get_ai(GeneticHistory.get(ai_id))
        history_list = GeneticHistory.objects.filter(id__gte=17189,
                                                     id__lte=28079,
                                                     profit__gte=10200000)
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "【BASE】第{}世代AI[id:{}]".format(base_ai.generation, base_ai.pk)
        for history in history_list:
            ai = AI2EurUsd.get_ai(history)
            dupe_point = get_dupe_point(base_ai, ai)
            print "SCORE:%03d" % dupe_point, "第{}世代AI[id:{}]".format(ai.generation, ai.pk)
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


def get_dupe_point(a, b):
    """
    AIの類似度を調べる
    :param a: AI
    :param b: AI
    :rtype : int
    """
    point = 0
    for key in a.ai_dict:
        if key in ('base_tick'):
            if a.ai_dict[key] == b.ai_dict[key]:
                point += 100
            else:
                continue
        if key in ('depth'):
            if a.ai_dict[key] == b.ai_dict[key]:
                point += 1000
            else:
                continue
        if a.ai_dict[key] == b.ai_dict[key]:
            point += 1
    return point