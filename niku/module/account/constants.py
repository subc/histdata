# -*- coding: utf-8 -*-
"""
https://docs.google.com/spreadsheets/d/1yTo-NvOdio7ya3WFnvAI12swvwNWMLIs8mheycyo7Aw/edit#gid=0
"""
from __future__ import absolute_import
from __future__ import unicode_literals


# 証拠金係数
MARGIN_COEFFICIENT = 37.5

# 1日のリスク係数
DAILY_RISK_COEFFICIENT = 0.75

UNITS = 200


def get_units(daily_risk, ai_count):
    """
    最適なユニット数を返却

    count * units * risk_coeff = daily_risk
    units = daily_risk / count / risk_coeff

    :param daily_risk: int
    :param ai_count: int
    :rtype : int
    """
    return int(daily_risk / ai_count / DAILY_RISK_COEFFICIENT)
