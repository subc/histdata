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
    class Meta(object):
        abstract = True

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


class OandaAccountAPIBase(object):
    """
    リトライなしのAPI
    """
    class Meta(object):
        abstract = True

    def __init__(self, mode, account):
        """
        :param mode: OandaAPIMode
        :param account: string
        """
        self.mode = mode
        self.account = account

    def requests_api(self, url, payload=None):
        if payload:
            print 'PAYLOAD IS {}'.format(payload)
            requests.adapters.DEFAULT_RETRIES = 1  # 最大1回
            response = requests.post(url, headers=self.mode.headers, data=payload)
        else:
            response = requests.get(url, headers=self.mode.headers)

        if not response.status_code == 200:
            print response.text
        try:
            assert response.status_code == 200, response.status_code
            print 'API_TEST: {}'.format(url)
            data = ujson.loads(response.text)
            self.check_json(data)
        except AssertionError:
            raise TypeError, response.text
        return data

    def check_json(self, data):
        raise NotImplementedError


class OandaAPIModelBase(object):
    pass