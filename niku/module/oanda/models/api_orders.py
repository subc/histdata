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

    def post(self, order):
        """
        :param order: Order
        :rtype : OrderApiModels
        """
        if self.mode == OandaAPIMode.DUMMY:
            return OrderApiModels.get_dummy(order)

        url = self.url_base.format(self.mode.url_base, self.account)
        payload = {
            'instrument': order.currency_pair.name,
            'units': order.units,
            'side': order.side,
            'type': 'market',
            'takeProfit': order.limit_rate,
            'stopLoss': order.stop_limit_rate,
            'lowerBound': order.lowerBound,
            'upperBound': order.upperBound,
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
    tradeOpened = None

    def __init__(self, data):
        self.instrument = str(data.get('instrument'))
        _time = data.get('time')
        self.time = parse_time(_time) if type(_time) == str else _time
        self.price = float(data.get('price'))
        _tradeOpened = data.get('tradeOpened')
        self.tradeOpened = TradeOpened(_tradeOpened) if type(_tradeOpened) == dict else _tradeOpened
        self._check(data)

    @classmethod
    def get_dummy(cls, order):
        """
        :param order: Order
        :rtype : OrderApiModels
        """
        data = {
            'instrument': order.currency_pair.name,
            'time': order.created_at,
            'price': order.open_rate,
            'tradeOpened': TradeOpened.get_dummy(order)
        }
        return cls(data)

    def _check(self, price):
        if 'tradeOpened' not in price:
            raise ValueError
        if 'price' not in price:
            raise ValueError
        if 'time' not in price:
            raise ValueError
        if 'instrument' not in price:
            raise ValueError


class TradeOpened(OandaAPIModelBase):
    oanda_ticket_id = None
    units = None
    side = None
    takeProfit = None
    stopLoss = None
    trailingStop = None

    def __init__(self, data):
        self.oanda_ticket_id = int(data.get('id'))
        self.units = int(data.get('units'))
        self.side = str(data.get('side'))
        self.takeProfit = float(data.get('takeProfit'))
        self.stopLoss = float(data.get('stopLoss'))
        self.trailingStop = float(data.get('trailingStop'))
        self._check(data)

    @classmethod
    def get_dummy(cls, order):
        """
        :param order: Order
        :rtype : OrderApiModels
        """
        data = {
            'id': 0,
            'units': order.units,
            'side': order.side,
            'takeProfit': order.limit_rate,
            'stopLoss': order.stop_limit_rate,
            'trailingStop': 0,
        }
        return cls(data)

    def _check(self, price):
        if 'id' not in price:
            raise ValueError
        if 'units' not in price:
            raise ValueError
        if 'side' not in price:
            raise ValueError
        if 'takeProfit' not in price:
            raise ValueError
        if 'stopLoss' not in price:
            raise ValueError
        if 'trailingStop' not in price:
            raise ValueError
