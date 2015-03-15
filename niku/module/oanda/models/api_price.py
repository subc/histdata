# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from .base import OandaAPIBase, OandaAPIModelBase
from module.rate import CurrencyPair


class PriceAPI(OandaAPIBase):
    """
    注文を取る

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
    """
    @classmethod
    def get_all(cls):
        instruments = '%2'.join([x.name for x in CurrencyPair])
        print instruments

    pass


class PriceAPIModel(OandaAPIModelBase):
    instrument = None
    time = None
    bid = None
    ask = None
    status = None