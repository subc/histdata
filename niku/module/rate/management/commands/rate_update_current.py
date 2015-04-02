# -*- coding: utf-8 -*-
"""
直近のレートを更新する
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.core.management import BaseCommand
import requests
from module.rate import CurrencyPair, CurrencyPairToTable
from module.rate.models import CandleEurUsdM5Rate
from module.rate.models.eur import Granularity, CandleEurUsdM1Rate
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
from line_profiler import LineProfiler


MODE = {
    'sandbox': 'api-sandbox.oanda.com',
    'production': 'api-fxtrade.oanda.com',
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        # 直近のレート取得
        now = datetime.datetime.now(pytz.utc)
        seven_days_ago = now - datetime.timedelta(seconds=3600*24*1)
        for pair in CurrencyPair:
            print 'START :{}'.format(pair)
            self.update_rate(pair, Granularity.D, 700, limit=seven_days_ago)
            self.update_rate(pair, Granularity.H1, 100, limit=seven_days_ago)
            self.update_rate(pair, Granularity.M5, 15, limit=seven_days_ago)
            self.update_rate(pair, Granularity.M1, 2, limit=seven_days_ago)
            self.update_ma(pair)

    def update_rate(self, currency_pair, granularity, span, limit=None):
        """
        :param currency_pair: CurrencyPair
        :param granularity: Granularity
        """
        for _date in start_date_generator(span, limit=limit):
            start = '%02d-%02d-%02d' % (int(_date.year), int(_date.month), int(_date.day))
            # レート取得
            base_domain = MODE.get('production')
            url_base = 'https://{}/v1/candles?'.format(base_domain)
            url = url_base + 'instrument={}&'.format(currency_pair.name) + \
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
            CurrencyPairToTable.get_table(currency_pair, granularity).safe_bulk_create_by_oanda(candles, start_at=limit)

    def update_ma(self, pair):
        """
        MA更新
        """
        seven_days_ago = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
        ma_cls = CurrencyPairToTable.get_ma_table(pair)
        ma_cls.sync(seven_days_ago, pair)


def requests_api(url, payload=None):
    auth = 'Bearer {}'.format(get_password('OandaRestAPIToken'))
    headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Accept': '*/*', 'User-Agent': 'python-requests/1.2.0',
               'Content-type': 'application/json; charset=utf-8',
               'Authorization': auth}
    if payload:
        requests.adapters.DEFAULT_RETRIES = 2
        response = requests.post(url, headers=headers, data=payload, timeout=10)
    else:
        requests.adapters.DEFAULT_RETRIES = 2
        response = requests.get(url, headers=headers, timeout=10)
    print 'API_TEST: {}'.format(url)
    return response


def start_date_generator(span, limit=None):
    """
    現在から2005年までの日付を100日毎に返却する
    """
    now = datetime.datetime.now(pytz.utc)
    if limit is None:
        limit = datetime.datetime(2005, 1, 1, 0, 0, 0)
    span = datetime.timedelta(days=span)
    while now > limit:
        now = now - span
        yield now
