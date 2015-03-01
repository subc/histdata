# -*- coding: utf-8 -*-
"""
Rate Update
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.core.management import BaseCommand
import requests
from module.rate.models import CandleEurUsdM5Rate
from module.rate.models.eur import Granularity
from module.title.models.title import TitleSettings
from module.oanda.models.candle import OandaCandle
from utils import get_password
from utils.timeit import timeit
from utils.oanda_api import OandaAPI, Streamer
import ujson
import pytz
import requests
import random
import datetime


MODE = {
    'sandbox': 'api-sandbox.oanda.com',
    'production': 'api-fxtrade.oanda.com',
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        # レート取得
        # self.update_rate(Granularity.D, 700)
        # self.update_rate(Granularity.H1, 100)
        self.update_rate(Granularity.M5, 15)
        self.update_rate(Granularity.M1, 2)

    def update_rate(self, granularity, span):
        """
        :param granularity: Granularity
        """
        for _date in start_date_generator(span):
            start = '%02d-%02d-%02d' % (int(_date.year), int(_date.month), int(_date.day))
            # レート取得
            base_domain = MODE.get('production')
            url_base = 'https://{}/v1/candles?'.format(base_domain)
            url = url_base + 'instrument=EUR_USD&' + \
                'count=5000&' +\
                'candleFormat=midpoint&' +\
                'granularity={}&'.format(granularity.name) +\
                'dailyAlignment=0&' +\
                'alignmentTimezone=Asia%2FTokyo&' +\
                'start={}T00%3A00%3A00Z'.format(start)

            response = requests_api(url)
            assert response.status_code == 200, response.status_code
            data = ujson.loads(response.text)
            assert 'code' not in data
            candles = []
            for candle in data.get('candles'):
                candles.append(OandaCandle(candle, granularity))
            granularity.db_table_class.safe_bulk_create_by_oanda(candles)


def requests_api(url, payload=None):
    auth = 'Bearer {}'.format(get_password('OandaRestAPIToken'))
    headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Accept': '*/*', 'User-Agent': 'python-requests/1.2.0',
               'Content-type': 'application/json; charset=utf-8',
               'Authorization': auth}
    if payload:
        response = requests.post(url, headers=headers, data=payload)
    else:
        response = requests.get(url, headers=headers)
    print 'API_TEST: {}'.format(url)
    return response


def start_date_generator(span):
    """
    現在から2003年までの日付を100日毎に返却する
    """
    now = datetime.datetime.now()
    limit = datetime.datetime(2005, 1, 1, 0, 0, 0)
    span = datetime.timedelta(days=span)
    # now = now + span - datetime.timedelta(days=1)
    while now > limit:
        now = now - span
        yield now
