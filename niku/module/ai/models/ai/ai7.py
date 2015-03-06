# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from ..base import AI6EurUsd


class AI7EurUsd(AI6EurUsd):
    """
    DrawDownを基準にした動作を行う
    """
    ai_id = 7

    def score(self, correct_value):
        """
        性能値を返却
        グループ中の下位5個の性能平均をスコアとする

        correct_valueは補正値だけど、このAIは使わない
        :param correct_value: float
        :rtype : int
        """
        return int(sum(sorted(self.market.monthly_profit_group, key=lambda x: x)[:5]) / 5) - correct_value
