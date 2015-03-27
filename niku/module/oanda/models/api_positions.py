# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import urllib
from django.utils.functional import cached_property
from .base import OandaAPIModelBase, OandaAccountAPIBase
from module.rate import CurrencyPair
from utils.utc_to_jst import parse_time


class PositionsAPI(OandaAccountAPIBase):
    """
    現在のポジション一覧を取得

    curl -H "Authorization: Bearer ####" https://api-fxtrade.oanda.com/v1/accounts/######/positions

    {
        "positions" : [
            {
                "instrument" : "AUD_USD",
                "units" : 100,
                "side" : "sell",
                "avgPrice" : 0.78216
            },
            {
                "instrument" : "GBP_USD",
                "units" : 100,
                "side" : "sell",
                "avgPrice" : 1.49128
            },
            {
                "instrument" : "USD_JPY",
                "units" : 850,
                "side" : "buy",
                "avgPrice" : 119.221
            }
    }

    :rtype : dict of PositionsAPIModel
    """
    url_base = '{}v1/accounts/{}/positions'

    def get_all(self):
        url = self.url_base.format(self.mode.url_base, self.account)
        print url
        data = self.requests_api(url)
        d = {}
        for price in data.get('positions'):
            price_model = PositionsAPIModel(price)
            d[price_model.currency_pair] = price_model
        return d

    def check_json(self, data):
        assert 'positions' in data


class PositionsAPIModel(OandaAPIModelBase):
    instrument = None
    units = None
    side = None
    avgPrice = None
    _data = None

    def __init__(self, price):
        self.instrument = str(price.get('instrument'))
        self.units = int(price.get('units'))
        self.side = str(price.get('side'))
        self.avgPrice = float(price.get('avgPrice'))

        self._check(price)

    def _check(self, price):
        if 'instrument' not in price:
            raise ValueError
        if 'units' not in price:
            raise ValueError
        if 'side' not in price:
            raise ValueError
        if 'avgPrice' not in price:
            raise ValueError
        self.currency_pair

    def equals_units(self, units):
        if self.is_buy:
            return self.units == units
        elif self.is_sell:
            return self.units * -1 == units
        raise ValueError

    @cached_property
    def currency_pair(self):
        """
        :rtype : CurrencyPair
        """
        for pair in CurrencyPair:
            if str(pair.name) == str(self.instrument):
                return pair
        raise ValueError

    @property
    def is_buy(self):
        return self.side == str('buy')

    @property
    def is_sell(self):
        return self.side == str('sell')