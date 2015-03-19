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
        :return:
        """
        url = self.url_base.format(self.mode.url_base, self.account)
        payload = ujson.dumps({
            'instrument': order.currency_pair,
            'units': 100,
            'side': order.side,
            'type': 'market',
            'takeProfit': order.limit_rate,
            'stopLoss': order.stop_limit_rate,
            'lowerBound': order.lowerBound,
            'upperBound': order.upperBound,
        })
        data = self.requests_api(url, payload=payload)
        # dataをパースする
        print data
        return data

    def check_json(self, data):
        assert 'tradeOpened' in data
        assert 'time' in data
        assert 'price' in data
