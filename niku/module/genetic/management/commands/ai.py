# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand, CommandError
import requests
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

MODE = {
    'sandbox': 'api-sandbox.oanda.com',
    'production': 'api-fxtrade.oanda.com',
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        history_id = self._parse_args(args)
        self.run(history_id)

    def _parse_args(self, args):
        if len(args) != 1:
            raise CommandError(u'Usage: manage.py gen_serial <campaign-name> <serial-count> --settings=<your-settings-file>')
        history_id = int(args[0])

        return history_id

    def run(self, history_id):
        history = GeneticHistory.objects.get(id=history_id)
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'STATUS'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print '取引回数: {}'.format(len(history.ai.get('MARKET').get('positions')))

        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'AI LOGIC'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print history.ai.get('AI_LOGIC')

        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'MARKET'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print history.ai.get('MARKET')

        # for x in CandleEurUsdH1Rate.get_test_data2():
        #     print x.start_at, x.open_bid, x.close_bid, x.high_bid, x.low_bid