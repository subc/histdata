# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import urllib
from django.utils.functional import cached_property
from .base import OandaAPIBase, OandaAPIModelBase, OandaAccountAPIBase
from module.rate import CurrencyPair
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_orders import OrderApiModels
from utils.utc_to_jst import parse_time


class TransactionsAPI(OandaAccountAPIBase):
    """
    発注状況を調べる

    {
    "id" : 1789500620,
    "accountId" : *****,
    "time" : "2015-03-20T11:11:59.000000Z",
    "type" : "MARKET_ORDER_CREATE",
    "instrument" : "USD_JPY",
    "units" : 100,
    "side" : "buy",
    "price" : 121.085,
    "lowerBound" : 121.041,
    "upperBound" : 121.101,
    "takeProfitPrice" : 122.261,
    "stopLossPrice" : 120.901,
    "pl" : 0,
    "interest" : 0,
    "accountBalance" : 299999.0973,
    "tradeOpened" : {
    "id" : 1789500620,
    "units" : 100
    }
    },
    
    
    
    {
         "id" : 1789536248,
         "accountId" : *****,
         "time" : "2015-03-20T12:17:06.000000Z",
         "type" : "TAKE_PROFIT_FILLED",
         "tradeId" : 1789531428,
         "instrument" : "USD_JPY",
         "units" : 1,
         "side" : "sell",
         "price" : 121.017,
         "pl" : 0.02,
         "interest" : 0,
         "accountBalance" : 299999.1173
    },
    
              {
         "id" : 1789560748,
         "accountId" : *****,
         "time" : "2015-03-20T12:49:38.000000Z",
         "type" : "STOP_LOSS_FILLED",
         "tradeId" : 1789500620,
         "instrument" : "USD_JPY",
         "units" : 100,
         "side" : "sell",
         "price" : 120.899,
         "pl" : -18.6,
         "interest" : 0,
         "accountBalance" : 299980.3023
    },

    curl -H "Authorization: Bearer ************" https://api-fxtrade.oanda.com/v1/accounts/****/transactions
    """
    url_base = '{}v1/accounts/{}/transactions'

    def get_all(self):
        if self.mode == OandaAPIMode.DUMMY:
            return {}
        url = self.url_base.format(self.mode.url_base, self.account)
        data = self.requests_api(url)
        transactions = data.get('transactions')
        if not transactions:
            return []
        r = []
        for transaction in transactions:
            r.append(TransactionsAPIModel(transaction))
        print r

    def check_json(self, data):
        if 'transactions' not in data:
            raise AssertionError


class TransactionsAPIModel(OandaAPIModelBase):
    oanda_ticket_id = None
    accountId = None
    order_type = None
    time = None
    tradeId = None  # 注文系トランザクションにだけ付く
    _data = None

    def __init__(self, data):
        self.oanda_ticket_id = data.get('id')
        self.accountId = data.get('accountId')
        self.order_type = data.get('order_type')
        self.time = parse_time(data.get('time'))
        if 'tradeId' in data:
            self.tradeId = data.get('tradeId')
        self._data = data