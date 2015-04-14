# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


class MarketTimeMixin(object):
    @classmethod
    def holiday(cls, _d):
        """
        日本時間で
        金曜日24:00〜月曜9:00ならTrue

        UTCで
        金曜日15:00〜月曜0:00ならTrue
        :param _d: datetime
        """
        key = _d.date().weekday() * 100 + _d.hour
        return key >= 415

    @classmethod
    def newyear(cls, _d):
        """
        UTCで
        12/20 0:00 〜 1/5 0:00
        :param _d: datetime
        """
        key = _d.month * 100 + _d.day
        return not(104 < key < 1220)