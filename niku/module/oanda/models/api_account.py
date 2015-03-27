# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import urllib
from django.utils.functional import cached_property
from .base import OandaAPIBase, OandaAPIModelBase, OandaAccountAPIBase
from module.rate import CurrencyPair
from utils.utc_to_jst import parse_time


class AccountAPI(OandaAccountAPIBase):
    """
    アカウント情報

    curl -H "Authorization: Bearer ********" https://api-fxtrade.oanda.com/v1/accounts/####
    {
        "accountId" : ###3,
        "accountName" : "Primary",
        "balance" : 123456.5765,
        "unrealizedPl" : 36.8816,
        "realizedPl" : 235.5839,
        "marginUsed" : 16529.154,
        "marginAvail" : 123450.3041,
        "openTrades" : 20,
        "openOrders" : 0,
        "marginRate" : 0.04,
        "accountCurrency" : "JPY"
    }

    :rtype : dict of PriceAPIModel
    """
    url_base = '{}v1/accounts/{}'

    def get_all(self):
        url = self.url_base.format(self.mode.url_base, self.account)
        data = self.requests_api(url)
        return data

    def check_json(self, data):
        assert 'accountId' in data
        assert 'balance' in data
