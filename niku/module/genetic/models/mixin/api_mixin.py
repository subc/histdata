# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import requests
import ujson
import sys


class ApiMixin(object):
    """
    API通信を行うMixin
    """
    def history_write(self, ai_group):
        """
        HTTP通信で書き込む
        """
        url_base = 'http://{}/genetic/history/'

        print ai_group[0].ai_dict
        payload = ujson.dumps({
            'ai_group': [ai.to_dict() for ai in ai_group],
        })
        response = requests_post_api(url_base, payload=payload)
        assert response.status_code == 200, response.text

    def history_back_test_write(self, ai_group):
        """
        HTTP通信で書き込む
        """
        url_base = 'http://{}/genetic/history/back_test'
        payload = ujson.dumps({
            'ai_group': [ai.to_dict() for ai in ai_group],
        })
        response = requests_post_api(url_base, payload=payload, log=False)
        assert response.status_code == 200, response.text


def requests_post_api(url_base, payload=None, log=True):
    if log:
        print "~~~~~~~~~~~~~~~~~~~~~~~~"
        print payload
        print "~~~~~~~~~~~~~~~~~~~~~~~~"
        print "POST PARAM SIZE:{}".format(sys.getsizeof(payload))

    TEST_HOST = '127.0.0.1:8000'
    url = url_base.format(TEST_HOST)
    payload = {'data': payload}
    requests.adapters.DEFAULT_RETRIES = 100
    response = requests.post(url, data=payload)
    print 'URL SUCCESS: {}'.format(url)
    return response
