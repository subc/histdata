# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


class CandleTypeMixin(object):
    """
    ローソク足のタイプ分類機能を付与
    """

    def get_candle_type(self, base_tick):
        """
        :param base_tick: int
        :rtype : int
        """
        return CandlePattern.get(get_type(self, base_tick), 999)


def get_type(rate, p):
    """
    :param rate: Rate
    :param p: int
    """
    tick = rate.tick
    p_high = get_type_by_diff((rate.high_bid - rate.open_bid) / tick, p)
    p_low = get_type_by_diff((rate.low_bid - rate.open_bid) / tick, p)
    p_close = get_type_by_diff(int((rate.close_bid - rate.open_bid) / tick), p)
    return p_high * 100 + p_low * 10 + p_close


def get_type_by_diff(_d, p):
    """
    :param _d: int
    :param : int
    """
    if _d >= p * 2:
        return 5
    if _d <= p * -2:
        return 1
    if p * 2 > _d >= p:
        return 4
    if p > _d > p * -1:
        return 3
    if p * -1 >= _d > p * -2:
        return 2
    raise ValueError


"""
op(開始時のレート)を3として、bp(base tick)
op - bp <= rate <= op + bp の範囲は3
op - 2bp <= rate < op - bp の範囲は2
rate < op - 2bp の範囲は1
op + bp < rate <= op + 2bp の範囲は4
2bp < rate  の範囲は5

例) keyが311 なら
high が3（opと同じレンジ）
low が1
close が1
valueの1は、CandlePatterID
"""
CandlePattern = {
    311: 1,
    312: 2,
    313: 3,
    322: 7,
    323: 8,
    333: 13,
    411: 16,
    412: 17,
    413: 18,
    414: 19,
    422: 22,
    423: 23,
    424: 24,
    433: 28,
    434: 29,
    511: 31,
    512: 32,
    513: 33,
    514: 34,
    515: 35,
    522: 37,
    523: 38,
    524: 39,
    525: 40,
    533: 43,
    534: 44,
    535: 45,
}