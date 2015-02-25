# -*- coding: utf-8 -*-
"""
テスト1
最適な値を1時間足から計算
"""
from __future__ import absolute_import
from __future__ import unicode_literals


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
    1: [1, 20, 20],
    2: [1, 20, 20],
    3: [2, 20, 20],
    4: [3, 20, 20],
    5: [3, 20, 20],
    6: [1, 20, 20],
    7: [1, 20, 20],
    8: [2, 20, 20],
    9: [3, 20, 20],
    10: [3, 20, 20],
    11: [1, 20, 20],
    12: [1, 20, 20],
    13: [2, 20, 20],
    14: [3, 20, 20],
    15: [3, 20, 20],
    16: [1, 20, 20],
    17: [1, 20, 20],
    18: [2, 20, 20],
    19: [3, 20, 20],
    20: [3, 20, 20],
    21: [1, 20, 20],
    22: [1, 20, 20],
    23: [2, 20, 20],
    24: [3, 20, 20],
    25: [3, 20, 20],
    26: [1, 20, 20],
    27: [1, 20, 20],
    28: [2, 20, 20],
    29: [3, 20, 20],
    30: [3, 20, 20],
    31: [1, 20, 20],
    32: [1, 20, 20],
    33: [2, 20, 20],
    34: [3, 20, 20],
    35: [3, 20, 20],
    36: [1, 20, 20],
    37: [1, 20, 20],
    38: [2, 20, 20],
    39: [3, 20, 20],
    40: [3, 20, 20],
    41: [1, 20, 20],
    42: [1, 20, 20],
    43: [2, 20, 20],
    44: [3, 20, 20],
    45: [3, 20, 20],
}