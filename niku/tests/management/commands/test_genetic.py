# -*- coding: utf-8 -*-
"""
Django標準adminのURLを試験する
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import random
import ujson
from django.core.management import BaseCommand
import requests
from ...constans import TEST_HEADER, TEST_HOST


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        url_base = 'http://{}/genetic/history/'
        payload = ujson.dumps({
            'ai_group': [AI().to_dict() for x in xrange(10)],
        })
        response = requests_api(url_base, payload=payload)
        assert response.status_code == 200, response.text

        # url_base = 'http://{}/genetic/history/back_test'
        # payload = ujson.dumps({
        #     'genetic_id': 179,
        # })
        # response = requests_api(url_base, payload=payload)
        # assert response.status_code == 200, response.text


def requests_api(url_base, payload=None):
    url = url_base.format(TEST_HOST)
    if payload:
        payload = {'data': payload}
        response = requests.post(url, data=payload)
    else:
        response = requests.get(url, headers=TEST_HEADER)
    print 'URL SUCCESS: {}'.format(url)
    return response


class AI(object):
    name = 'sample data',
    generation = 1,
    profit = random.randint(1, 2000),
    profit_max = 10000,
    profit_min = 100,
    # ai = {x: x ^ 2 for x in xrange(10)}
    ai = {'NAME': 1,
          'GENERATION': 1,
          'PROFIT': 1,
          'PROFIT_MAX': 1,
          'PROFIT_MIN': 1,
          'AI_LOGIC': {},
          'MARKET': 1,
          'CURRENCY_PAIR': 1,
          'END_AT': 1,
          'TRADE_COUNT': 1,
          'GENETIC_HISTORY_ID': 0,
    }

    def to_dict(self):
        return {'NAME': 1,
                'GENERATION': 1,
                'PROFIT': 1,
                'PROFIT_MAX': 1,
                'PROFIT_MIN': 1,
                'AI_LOGIC': {},
                'MARKET': 1,
                'CURRENCY_PAIR': 1,
                'END_AT': 1,
                'TRADE_COUNT': 1,
                'GENETIC_HISTORY_ID': 0,
        }