# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from utils.utc_to_jst import parse_time
from enum import Enum


class Granularity(Enum):
    H1 = 60 * 60
    M5 = 60 * 5


class OandaCandle(object):
    """
    v1/candles APIで取得するOANDAのキャンドルデータ

    例)
     u'complete': False, # Trueのときまだ続きがある
     u'closeMid': 1.24059,
     u'highMid': 1.24059,
     u'lowMid': 1.240575,
     u'volume': 6,
     u'openMid': 1.240585,
     u'time': u'2015-02-23T15:10:00.000000Z' UTC

    # ドキュメント
    http://developer.oanda.com/rest-live/rates/#getCurrentPrices
    """
    complete = None
    openMid = None
    closeMid = None
    highMid = None
    lowMid = None
    volume = None
    c_time = None
    _time = None
    granularity = None  # キャンドルの幅

    def __init__(self, _data, granularity):
        """
        :param _data: dict
        :param granularity: Granularity
        """
        self._data = _data
        self.complete = bool(_data.get('complete'))
        self.openMid = float(_data.get('openMid'))
        self.closeMid = float(_data.get('closeMid'))
        self.highMid = float(_data.get('highMid'))
        self.lowMid = float(_data.get('lowMid'))
        self.volume = float(_data.get('volume'))
        self._time = _data.get('time')
        self.c_time = parse_time(self._time)
        self.granularity = granularity
        self.check()

    def __unicode__(self):
        return '{}:open:{}'.format(self.c_time, self.openMid)

    def check(self):
        """
        値が正しいことを確認する
        """
        if not self.openMid:
            raise ValueError

        if not self.closeMid:
            raise ValueError

        if not self.highMid:
            raise ValueError

        if not self.lowMid:
            raise ValueError

        if not self.c_time:
            raise ValueError

        if not self.granularity:
            raise ValueError

        if not self._time:
            raise ValueError

        if type(self.granularity) != Granularity:
            raise TypeError
