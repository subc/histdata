# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import requests
import time
import ujson


class HttpError(Exception):
    pass


class OandaAPIBase(object):
    mode = None

    def __init__(self, mode):
        """
        :param mode: OandaAPIMode
        """
        self.mode = mode

    def requests_api(self, url, payload=None):
        # 3回繰り返す
        for x in xrange(3):
            try:
                if payload:
                    response = requests.post(url, headers=self.mode.headers, data=payload)
                else:
                    response = requests.get(url, headers=self.mode.headers)

                assert response.status_code == 200, response.status_code
                print 'API_TEST: {}'.format(url)
                data = ujson.loads(response.text)
                self.check_json(data)
                return data
            except:
                print 'http error'
                time.sleep(3)
                pass
        raise HttpError

    def check_json(self, data):
        raise NotImplementedError


class OandaAPIModelBase(object):
    pass