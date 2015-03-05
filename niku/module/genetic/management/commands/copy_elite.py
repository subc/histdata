# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand, CommandError
import requests
from module.genetic.models import GeneticHistory, GeneticBackTestHistory
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
        self.run()

    def run(self):
        num = GeneticBackTestHistory.create_test_story()
        print "COPY ELITE COUNT:{}".format(num)

        # UPDATE
        count = GeneticHistory.objects.filter(elite=None).update(elite=0)
        print "UPDATE HISTORY RECORD ELITE NULL TO 0:{}".format(count)