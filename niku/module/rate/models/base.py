# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models
from django.utils.functional import cached_property
from .candle_type import CandleTypeMixin


class CurrencyCandleBase(CandleTypeMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    open_bid = models.FloatField()
    close_bid = models.FloatField()
    high_bid = models.FloatField()
    low_bid = models.FloatField()
    volume = models.FloatField(default=0, help_text='取引量')
    start_at = models.DateTimeField(db_index=True, help_text='開始時間')
    interval = models.PositiveIntegerField(default=0)
    _granularity = None

    class Meta(object):
        app_label = 'rate'
        abstract = True
        unique_together = ('start_at',)

    @classmethod
    def get(cls, pk):
        """
        :return: CurrencyCandleBase
        """
        return cls.objects.get(id=pk)

    @classmethod
    def get_all(cls):
        """
        :return: list of CurrencyCandleBase
        """
        return cls.sort(list(cls.objects.filter()))

    @classmethod
    def create(cls, **kwargs):
        """
        insertする
        :return: CurrencyCandleBase
        """
        cls.objects.create(**kwargs)

    @classmethod
    def sort(cls, candles):
        return sorted(candles, key=lambda x: x.start_at)

    @classmethod
    def safe_bulk_create_by_oanda(cls, oanda_candles):
        """
        Duplicate errorが発生しない安全なcreate
        :param oanda_candles: list of OandaCandle
        :rtype : bool
        """
        candle_dict = {str(candle.c_time): candle for candle in oanda_candles}
        register_candles = [str(candle.start_at) for candle in list(cls.objects.filter())]
        # print register_candles
        # print candle_dict
        for register_candle in register_candles:
            if register_candle in candle_dict:
                del candle_dict[register_candle]
        if candle_dict:
            cls.bulk_create_by_oanda(candle_dict.values())
        return True

    @classmethod
    def bulk_create_by_oanda(cls, oanda_candles):
        """
        :param oanda_candles: list of OandaCandle
        :rtype : bool
        """
        cls.objects.bulk_create([cls.convert_oanda_to_candle(_candle) for _candle in oanda_candles])
        return True

    @classmethod
    def convert_oanda_to_candle(cls, oanda_candle):
        """
        :param oanda_candle: OandaCandle
        :rtype : CurrencyCandleBase
        """
        if oanda_candle.granularity != oanda_candle.granularity:
            raise ValueError
        return cls(open_bid=oanda_candle.openMid,
                   close_bid=oanda_candle.closeMid,
                   high_bid=oanda_candle.highMid,
                   low_bid=oanda_candle.lowMid,
                   volume=oanda_candle.volume,
                   start_at=oanda_candle.c_time,
                   interval=oanda_candle.granularity.value)

    @property
    def granularity(self):
        """
        キャンドル毎の間隔(秒)のEnum型
        :rtype : Granularity
        """
        if self._granularity is None:
            raise NotImplementedError
        return self._granularity


class MultiCandles(CandleTypeMixin):
    """
    複数のローソク足を透過的に扱うクラス
    """
    rates = None

    def __init__(self, rates):
        self.rates = rates

    @property
    def open_bid(self):
        return self.rates[0].open_bid

    @cached_property
    def high_bid(self):
        return max([r.high_bid for r in self.rates])

    @cached_property
    def low_bid(self):
        return min([r.low_bid for r in self.rates])

    @property
    def close_bid(self):
        return self.rates[-1].close_bid

    @property
    def tick(self):
        return self.rates[-1].tick