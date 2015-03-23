# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import urllib
from django.utils.functional import cached_property
from .base import OandaAPIBase, OandaAPIModelBase
from module.rate import CurrencyPair
from utils.utc_to_jst import parse_time


class PriceAPI(OandaAPIBase):
    """
    注文を取る

    %2C は　カンマ

    curl -H "Authorization: Bearer ********" -X GET "https://api-fxtrade.oanda.com/v1/prices?instruments=EUR_USD%2CUSD_JPY%2CEUR_CAD"

    {
        "prices" : [
            {
                "instrument" : "EUR_USD",
                "time" : "2015-03-13T20:59:58.165668Z",
                "bid" : 1.04927,
                "ask" : 1.04993,
                "status" : "halted"
            },
            {
                "instrument" : "USD_JPY",
                "time" : "2015-03-13T20:59:58.167818Z",
                "bid" : 121.336,
                "ask" : 121.433,
                "status" : "halted"
            },
            {
                "instrument" : "EUR_CAD",
                "time" : "2015-03-13T20:59:58.165465Z",
                "bid" : 1.34099,
                "ask" : 1.34225,
                "status" : "halted"
            }
        ]
    }

    :rtype : dict of PriceAPIModel
    """
    url_base = '{}v1/prices?'

    def get_all(self):
        instruments = ','.join([x.name for x in CurrencyPair])
        instruments = urllib.quote(instruments, '')
        url = self.url_base.format(self.mode.url_base)
        url += 'instruments={}'.format(instruments)
        data = self.requests_api(url)
        d = {}
        for price in data.get('prices'):
            price_model = PriceAPIModel(price)
            d[price_model.currency_pair] = price_model
        return d

    def check_json(self, data):
        assert 'prices' in data


class PriceAPIModel(OandaAPIModelBase):
    instrument = None
    time = None
    bid = None
    ask = None
    status = None

    def __init__(self, price):
        self.ask = float(price.get('ask'))
        self.bid = float(price.get('bid'))
        self.time = parse_time(price.get('time'))
        self.instrument = str(price.get('instrument'))
        if 'status' in price:
            self.status = str(price.get('status'))
        self._check(price)

    def _check(self, price):
        if 'ask' not in price:
            raise ValueError
        if 'bid' not in price:
            raise ValueError
        if 'time' not in price:
            raise ValueError
        if 'instrument' not in price:
            raise ValueError
        self.currency_pair

    @cached_property
    def currency_pair(self):
        """
        :rtype : CurrencyPair
        """
        for pair in CurrencyPair:
            if str(pair.name) == str(self.instrument):
                return pair
        raise ValueError

    @cached_property
    def is_maintenance(self):
        """
        メンテ中ならTrue
        :rtype : bool
        """
        if self.status is None:
            return False
        if str(self.status) == str('halted'):
            return True
        return False

    @cached_property
    def cost_tick(self):
        diff = self.ask - self.bid
        return float(diff / self.currency_pair.get_base_tick())

    def is_active(self):
        """
        有効なレートならTrue
        :rtype : bool
        """
        # メンテ中じゃない
        if self.is_maintenance:
            return False

        # レートが正常 4tickまで許容する
        if self.cost_tick > 4:
            return False
        return True
