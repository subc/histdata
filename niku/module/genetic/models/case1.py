# -*- coding: utf-8 -*-
"""
テスト1
最適な値を1時間足から計算
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from .parameter import OrderType


"""
311 なら
high が3
low が1
close が1
"""
LogicPatternCase1 = {
    311: 1,
    312: 2,
    313: 3,
    314: 4,
    315: 5,
    321: 6,
    322: 7,
    323: 8,
    324: 9,
    325: 10,
    331: 11,
    332: 12,
    333: 13,
    334: 14,
    335: 15,
    411: 16,
    412: 17,
    413: 18,
    414: 19,
    415: 20,
    421: 21,
    422: 22,
    423: 23,
    424: 24,
    425: 25,
    431: 26,
    432: 27,
    433: 28,
    434: 29,
    435: 30,
    511: 31,
    512: 32,
    513: 33,
    514: 34,
    515: 35,
    521: 36,
    522: 37,
    523: 38,
    524: 39,
    525: 40,
    531: 41,
    532: 42,
    533: 43,
    534: 44,
    535: 45,
}

"""
Buy が3 yieldが2 sellが1
利益確定が20
損切りが20
"""
AiBaseCase1 = {
    'base_tick': 20,
    1: [OrderType.SELL, 20, 20],
    2: [OrderType.SELL, 20, 20],
    3: [OrderType.WAIT, 20, 20],
    4: [OrderType.BUY, 20, 20],
    5: [OrderType.BUY, 20, 20],
    6: [OrderType.SELL, 20, 20],
    7: [OrderType.SELL, 20, 20],
    8: [OrderType.WAIT, 20, 20],
    9: [OrderType.BUY, 20, 20],
    10: [OrderType.BUY, 20, 20],
    11: [OrderType.SELL, 20, 20],
    12: [OrderType.SELL, 20, 20],
    13: [OrderType.WAIT, 20, 20],
    14: [OrderType.BUY, 20, 20],
    15: [OrderType.BUY, 20, 20],
    16: [OrderType.SELL, 20, 20],
    17: [OrderType.SELL, 20, 20],
    18: [OrderType.WAIT, 20, 20],
    19: [OrderType.BUY, 20, 20],
    20: [OrderType.BUY, 20, 20],
    21: [OrderType.SELL, 20, 20],
    22: [OrderType.SELL, 20, 20],
    23: [OrderType.WAIT, 20, 20],
    24: [OrderType.BUY, 20, 20],
    25: [OrderType.BUY, 20, 20],
    26: [OrderType.SELL, 20, 20],
    27: [OrderType.SELL, 20, 20],
    28: [OrderType.WAIT, 20, 20],
    29: [OrderType.BUY, 20, 20],
    30: [OrderType.BUY, 20, 20],
    31: [OrderType.SELL, 20, 20],
    32: [OrderType.SELL, 20, 20],
    33: [OrderType.WAIT, 20, 20],
    34: [OrderType.BUY, 20, 20],
    35: [OrderType.BUY, 20, 20],
    36: [OrderType.SELL, 20, 20],
    37: [OrderType.SELL, 20, 20],
    38: [OrderType.WAIT, 20, 20],
    39: [OrderType.BUY, 20, 20],
    40: [OrderType.BUY, 20, 20],
    41: [OrderType.SELL, 20, 20],
    42: [OrderType.SELL, 20, 20],
    43: [OrderType.WAIT, 20, 20],
    44: [OrderType.BUY, 20, 20],
    45: [OrderType.BUY, 20, 20],
}