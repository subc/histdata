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
        r = sorted(r, key=lambda x: x.oanda_transaction_id)
        return r

    def check_json(self, data):
        if 'transactions' not in data:
            raise AssertionError


class TransactionsAPIModel(OandaAPIModelBase):
    oanda_transaction_id = None
    accountId = None
    order_type = None
    time = None
    tradeId = None  # 注文系トランザクションにだけ付く
    accountBalance = None  # アカウントの残高
    _data = None

    def __init__(self, data):
        self.oanda_transaction_id = data.get('id', None)
        self.accountId = data.get('accountId')
        self.order_type = data.get('type')
        self.time = parse_time(data.get('time'))
        self.tradeId = data.get('tradeId', None)
        self.accountBalance = data.get('accountBalance', None)
        self._data = data

    @property
    def market_order_create(self):
        """
        :rtype :bool
        """
        return self.order_type == 'MARKET_ORDER_CREATE'

    @property
    def market_order_stop_limit(self):
        """
        :rtype :bool
        """
        return self.order_type in ['TAKE_PROFIT_FILLED', 'STOP_LOSS_FILLED']

    @property
    def profit(self):
        if not self.market_order_stop_limit:
            return None
        return float(self._data.get('pl'))

    @property
    def memo(self):
        if 'instrument' not in self._data:
            return ''

        if 'units' not in self._data:
            return ''

        if 'side' not in self._data:
            return ''
        instrument = str(self._data.get('instrument'))
        units = str(self._data.get('units'))
        side = str(self._data.get('side'))
        return ':'.join([instrument, side, units])