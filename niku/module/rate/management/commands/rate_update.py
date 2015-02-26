# -*- coding: utf-8 -*-
"""
Rate Update
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import requests
from module.rate.models import CandleEurUsdM5Rate
from module.rate.models.eur import Granularity
from module.title.models.title import TitleSettings
from module.oanda.models.candle import OandaCandle
from utils.timeit import timeit
from utils.oanda_api import OandaAPI, Streamer
import ujson
import pytz
import requests
import random

MODE = {
    'sandbox': 'api-sandbox.oanda.com',
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        # レート取得
        self.update_rate(Granularity.M5)
        self.update_rate(Granularity.H1)
        self.update_rate(Granularity.D)

    def update_rate(self, granularity):
        """
        :param granularity: Granularity
        """
        # レート取得
        base_domain = MODE.get('sandbox')
        url_base = 'https://{}/v1/candles?'.format(base_domain)
        url = url_base + 'instrument=EUR_USD&' + \
            'count=1&' +\
            'candleFormat=midpoint&' +\
            'granularity={}&'.format(granularity.name) +\
            'dailyAlignment=0&' +\
            'alignmentTimezone=Asia%2FTokyo&' +\
            'start=2001-06-19T15%3A40%3A00Z'

        response = requests_api(url)
        assert response.status_code == 200, response.status_code
        data = ujson.loads(response.text)
        assert 'code' not in data
        candles = []
        for candle in data.get('candles'):
            candles.append(OandaCandle(candle, granularity))
        granularity.db_table_class.safe_bulk_create_by_oanda(candles)


def requests_api(url, payload=None):
    auth = ''
    # headers = {'Content-type': 'application/json; charset=utf-8',
    #            'Authorization': auth,
    #            'User-Agent': 'mac'}
    headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Accept': '*/*', 'User-Agent': 'python-requests/1.2.0',
               'Content-type': 'application/json; charset=utf-8',}

    print url
    headers = {}
    if payload:
        response = requests.post(url, headers=headers, data=payload)
    else:
        response = requests.get(url, headers=headers)
    print 'API_TEST: {}'.format(url)
    return response