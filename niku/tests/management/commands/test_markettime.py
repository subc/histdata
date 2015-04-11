# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
import random
from django.core.management import BaseCommand
import pytz
import requests
from ...constans import TEST_HEADER, TEST_HOST
from django.core.management import BaseCommand
from module.board.models import AIBoard
from module.genetic.models.parameter import OrderType
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_orders import OrdersAPI
from module.oanda.models.api_price import PriceAPI
from module.rate import CurrencyPairToTable, Granularity
from utils.timeit import timeit


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        print "start"
        d = datetime.datetime(2010, 1, 1, tzinfo=pytz.utc)
        print self.benchmark(d)

    @timeit
    def benchmark(self, d):
        _d = d
        limit = datetime.datetime(2015, 1, 1, tzinfo=pytz.utc)
        scope = datetime.timedelta(seconds=3600)
        ct = 0
        while _d < limit:
            if MarketTime.holiday(_d):
                ct += 1
            if MarketTime.newyear(_d):
                ct += 1
            _d += scope
        return ct


class MarketTime(object):
    @classmethod
    def holiday(cls, _d):
        """
        日本時間で
        金曜日24:00〜月曜9:00ならTrue

        UTCで
        金曜日15:00〜月曜0:00ならTrue
        :param _d: datetime
        """
        key = _d.date().weekday() * 100 + _d.hour
        return key >= 415

    @classmethod
    def newyear(cls, _d):
        """
        UTCで
        12/20 0:00 〜 1/5 0:00
        :param _d: datetime
        """
        key = _d.month * 100 + _d.day
        return not(104 < key < 1220)