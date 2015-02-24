# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import requests
from ...constans import TEST_HEADER, TEST_HOST
from module.title.models.title import TitleSettings
from module.oanda.models.candle import OandaCandle, Granularity
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
        granularity = Granularity.M5
        base_domain = MODE.get('sandbox')
        url_base = 'https://{}/v1/candles?'.format(base_domain)
        url = url_base + 'instrument=EUR_USD&' + \
            'count=5000&' +\
            'candleFormat=midpoint&' +\
            'granularity={}&'.format(granularity.name) +\
            'dailyAlignment=0&' +\
            'alignmentTimezone=Asia%2FTokyo'    # 日足にだけ影響

        response = requests_api(url)
        assert response.status_code == 200, response.status_code
        data = ujson.loads(response.text)
        assert 'code' not in data
        for candle in data.get('candles'):
            OandaCandle(candle, granularity)


def requests_api(url, payload=None):
    auth = ''
    # headers = {'Content-type': 'application/json; charset=utf-8',
    #            'Authorization': auth,
    #            'User-Agent': 'mac'}
    print url
    headers = {}
    if payload:
        response = requests.post(url, headers=headers, data=payload)
    else:
        response = requests.get(url, headers=headers)
    print 'API_TEST: {}'.format(url)
    return response
