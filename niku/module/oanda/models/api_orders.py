# -*- coding: utf-8 -*-
"""
発注API
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import urllib
import ujson
from django.utils.functional import cached_property
from .base import OandaAccountAPIBase, OandaAPIModelBase
from module.oanda.constants import OandaAPIMode
from module.rate import CurrencyPair
from utils.utc_to_jst import parse_time


class OrdersAPI(OandaAccountAPIBase):
    """
    発注

    %2C は　カンマ

    curl -H "Authorization: Bearer ********"　-X POST -d "instrument=EUR_USD&units=2&side=sell&type=market" "https://api-fxtrade.oanda.com/v1/accounts/12345/orders"

    {

      "instrument" : "EUR_USD",
      "time" : "2013-12-06T20:36:06Z", // Time that order was executed
      "price" : 1.37041,               // Trigger price of the order
      "tradeOpened" : {
        "id" : 175517237,              // Order id
        "units" : 1000,                // Number of units
        "side" : "buy",                // Direction of the order
        "takeProfit" : 0,              // The take-profit associated with the Order, if any
        "stopLoss" : 0,                // The stop-loss associated with the Order, if any
        "trailingStop" : 0             // The trailing stop associated with the rrder, if any
      },
      "tradesClosed" : [],
      "tradeReduced" : {}
    }
    :rtype : dict of PriceAPIModel
    """
    url_base = '{}v1/accounts/{}/orders'

    def post(self, currency_pair, units):
        """
        :param currency_pair: CurrencyPair
        :param units: int
        :rtype : OrderApiModels
        """
        if self.mode == OandaAPIMode.DUMMY:
            return []

        url = self.url_base.format(self.mode.url_base, self.account)
        payload = {
            'instrument': currency_pair.name,
            'units': units if units > 0 else units * -1,
            'side': 'buy' if units > 0 else 'sell',
            'type': 'market',
        }
        data = self.requests_api(url, payload=payload)
        print data
        return OrderApiModels(data)

    def check_json(self, data):
        assert 'tradeOpened' in data
        assert 'time' in data
        assert 'price' in data


class OrderApiModels(OandaAPIModelBase):
    instrument = None
    time = None
    price = None

    def __init__(self, data):
        self.instrument = str(data.get('instrument'))
        _time = data.get('time')
        self.time = parse_time(_time) if type(_time) == str else _time
        self.price = float(data.get('price'))
        self._check(data)

    def _check(self, data):
        if 'price' not in data:
            raise ValueError
        if 'time' not in data:
            raise ValueError
        if 'instrument' not in data:
            raise ValueError