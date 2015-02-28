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
    1: [OrderType.WAIT, 20, 20],
    2: [OrderType.WAIT, 20, 20],
    3: [OrderType.WAIT, 20, 20],
    7: [OrderType.WAIT, 20, 20],
    8: [OrderType.WAIT, 20, 20],
    13: [OrderType.WAIT, 20, 20],
    16: [OrderType.WAIT, 20, 20],
    17: [OrderType.WAIT, 20, 20],
    18: [OrderType.WAIT, 20, 20],
    19: [OrderType.WAIT, 20, 20],
    22: [OrderType.WAIT, 20, 20],
    23: [OrderType.WAIT, 20, 20],
    24: [OrderType.WAIT, 20, 20],
    28: [OrderType.WAIT, 20, 20],
    29: [OrderType.WAIT, 20, 20],
    31: [OrderType.WAIT, 20, 20],
    32: [OrderType.WAIT, 20, 20],
    33: [OrderType.WAIT, 20, 20],
    34: [OrderType.WAIT, 20, 20],
    35: [OrderType.WAIT, 20, 20],
    37: [OrderType.WAIT, 20, 20],
    38: [OrderType.WAIT, 20, 20],
    39: [OrderType.WAIT, 20, 20],
    40: [OrderType.WAIT, 20, 20],
    43: [OrderType.WAIT, 20, 20],
    44: [OrderType.WAIT, 20, 20],
    45: [OrderType.WAIT, 20, 20],
}

# AiBaseCase1 = {
#     'base_tick': 15,
#     1: [OrderType.SELL, 12, 60],
#     2: [OrderType.SELL, 38, 22],
#     3: [OrderType.WAIT, 11, 48],
#     7: [OrderType.SELL, 7, 19],
#     8: [OrderType.WAIT, 33, 37],
#     13: [OrderType.WAIT, 24, 44],
#     16: [OrderType.SELL, 18, 60],
#     17: [OrderType.SELL, 57, 60],
#     18: [OrderType.WAIT, 28, 18],
#     19: [OrderType.BUY, 13, 46],
#     22: [OrderType.SELL, 29, 5],
#     23: [OrderType.WAIT, 27, 26],
#     24: [OrderType.BUY, 49, 5],
#     28: [OrderType.WAIT, 7, 28],
#     29: [OrderType.BUY, 60, 45],
#     31: [OrderType.SELL, 21, 52],
#     32: [OrderType.SELL, 11, 21],
#     33: [OrderType.WAIT, 24, 44],
#     34: [OrderType.BUY, 47, 40],
#     35: [OrderType.BUY, 43, 20],
#     37: [OrderType.SELL, 34, 60],
#     38: [OrderType.WAIT, 25, 53],
#     39: [OrderType.BUY, 15, 60],
#     40: [OrderType.BUY, 20, 5],
#     43: [OrderType.WAIT, 15, 5],
#     44: [OrderType.BUY, 31, 53],
#     45: [OrderType.BUY, 48, 5],
# }