# -*- coding: utf-8 -*-
"""
Rate Update
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
import time
from django.core.management import BaseCommand
import requests
from module.rate import CurrencyPair, CurrencyPairToTable
from module.rate.models import CandleEurUsdM5Rate
from module.oanda.constants import OandaAPIMode
from module.oanda.exceptions import OandaInternalServerError, OandaServiceUnavailableError
from module.oanda.models.base import OandaAPIBase
from module.rate.models.eur import Granularity
from module.title.models.title import TitleSettings
from module.oanda.models.candle import OandaCandle
from utils import get_password, CustomBaseCommand
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


class Command(CustomBaseCommand):
    def handle(self, *args, **options):
        try:
            self.run()
        except OandaServiceUnavailableError:
            # 土日メンテ中のとき
            self.echo("ServiceUnavailableError")
            time.sleep(60)
        except OandaInternalServerError:
            # 土日メンテ中のとき
            self.echo("OandaInternalServerError")
            time.sleep(60)

    def run(self):
        # レート取得
        for pair in CurrencyPair:
            self.update_rate(pair, Granularity.D, 700)
            self.update_rate(pair, Granularity.H1, 100)
            self.update_rate(pair, Granularity.M5, 15)
            self.update_rate(pair, Granularity.M1, 2, limit=datetime.datetime(2014, 1, 1, 0, 0, 0, tzinfo=pytz.utc))

    def update_rate(self, currency_pair, granularity, span, limit=None):
        """
        :param currency_pair: CurrencyPair
        :param granularity: Granularity
        """
        requests_api = OandaAPIBase(OandaAPIMode.PRODUCTION).requests_api
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

#
# def requests_api(url, payload=None):
#     auth = 'Bearer {}'.format(get_password('OandaRestAPIToken'))
#     headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
#                'Accept': '*/*', 'User-Agent': 'python-requests/1.2.0',
#                'Content-type': 'application/json; charset=utf-8',
#                'Authorization': auth}
#     if payload:
#         response = requests.post(url, headers=headers, data=payload)
#     else:
#         response = requests.get(url, headers=headers)
#     print 'API_TEST: {}'.format(url)
#     print response.text
#     return response


def start_date_generator(span, limit=None):
    """
    現在から2005年までの日付を100日毎に返却する
    """
    now = datetime.datetime.now(pytz.utc)
    if limit is None:
        limit = datetime.datetime(2005, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
    span = datetime.timedelta(days=span)
    while now > limit:
        now = now - span
        yield now
