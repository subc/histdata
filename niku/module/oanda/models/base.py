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
            response = requests.post(url, headers=self.mode.headers, data=payload)
        else:
            response = requests.get(url, headers=self.mode.headers)

        assert response.status_code == 200, response.status_code
        print 'API_TEST: {}'.format(url)
        data = ujson.loads(response.text)
        try:
            self.check_json(data)
        except AssertionError:
            self.hook_error(data)
            return data
        return data

    def check_json(self, data):
        raise NotImplementedError

    def hook_error(self, data):
        # todo ログに記録
        print 'エラー発生', data
        return


class OandaAPIModelBase(object):
    pass