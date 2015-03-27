# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from enum.enum import Enum
from utils import get_password


class OandaAPIMode(Enum):
    PRODUCTION = 1
    DEVELOP = 2
    SANDBOX = 3
    DUMMY = 4

    @property
    def url_base(self):
        api_base_url_dict = {
            OandaAPIMode.PRODUCTION: 'https://api-fxtrade.oanda.com/',
            OandaAPIMode.DEVELOP: 'https://api-fxpractice.oanda.com/',
            OandaAPIMode.SANDBOX: 'http://api-sandbox.oanda.com/',
        }
        return api_base_url_dict.get(self)

    @property
    def headers(self):
        """
        :rtype : dict
        """
        _base = {
            'Accept-Encoding': 'identity, deflate, compress, gzip',
            'Accept': '*/*', 'User-Agent': 'python-requests/1.2.0',
            'Content-type': 'application/x-www-form-urlencoded',
        }

        if self == OandaAPIMode.SANDBOX:
            return _base
        if self == OandaAPIMode.DEVELOP:
            _base['Authorization'] = 'Bearer {}'.format(get_password('OandaRestAPITokenDemo'))
            return _base
        if self == OandaAPIMode.PRODUCTION:
            _base['Authorization'] = 'Bearer {}'.format(get_password('OandaRestAPIToken'))
            return _base
        raise ValueError