# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import copy
import random

from ..base import AIInterFace, get_tick_category, convert_rate
from ..mixin import DispatchMixin
from module.currency import UsdJpyMixin
from module.genetic.models.parameter import OrderType
from module.rate import Granularity
from module.rate.models import CandleUsdJpyH1Rate
from module.rate.models.base import MultiCandles
from module.rate.models.usd import UsdJpyMA


class AIUsdJpyBase(DispatchMixin, UsdJpyMixin, AIInterFace):
    MUTATION_MAX = 120
    MUTATION_MIN = 10
    RATE_SPAN = Granularity.H1

    def score(self, correct_value):
        """
        性能値を返却
        期間を通しての利益で計算する

        correct_valueは補正値だけど、このAIは使わない
        :param correct_value: float
        :rtype : int
        """
        return self.profit - correct_value

    def set_start_data(self):
        return self

    def get_order_ai(self, market, prev_rates, open_bid, start_at):
        """
        条件に沿って注文する
        :param market: Market
        :param prev_rates: list of Rate
        :param open_bid: float
        :param start_at: datetime
        :rtype market: Market
        """
        rates = convert_rate(prev_rates, self.RATE_SPAN)

        if not rates:
            return None

        if len(rates) - 1 < self.depth:
            return None

        rate_type = self.get_key(open_bid, rates, start_at)

        # rateがNoneのとき注文しない
        if rate_type is None:
            return None

        if rate_type in self.ai_dict:
            order_type, limit, stop_limit = self.ai_dict.get(rate_type)
        else:
            # AIがない場合はデフォルトデータをロード
            self.ai_dict[rate_type] = [OrderType.get_random(), random.randint(20, 100), random.randint(20, 100)]
            order_type, limit, stop_limit = self.ai_dict.get(rate_type)
        from module.ai import OrderAI
        return OrderAI(order_type, limit, stop_limit)

    def normalization(self):
        """
        過剰最適化するAIの進化に制限を儲ける
        利確, 損切り 800pip先とかを禁止
        """
        ai = copy.deepcopy(self.ai_dict)
        for key in ai:
            if type(ai[key]) == list:
                for index in [1, 2]:
                    ai[key][index] = self.adjust(ai[key][index])
                continue
            ai[key] = self.adjust(ai[key])
        self.ai_dict = ai

    def adjust(self, value):
        if self.MUTATION_MAX < value:
            return self.MUTATION_MAX
        if self.MUTATION_MIN > value:
            return self.MUTATION_MIN
        return value

    def get_key(self, open_bid, rates, start_at):
        raise NotImplementedError


class AI1001UsdJpy(AIUsdJpyBase):
    ai_id = 1001
    MUTATION_MAX = 120
    MUTATION_MIN = 10

    def get_key(self, open_bid, rates, start_at):
        rate = rates[-1]
        if rate is None or rate.ma is None or rate.ma.h24 is None:
            return None

        # MA
        d5 = self.get_ma_key(rate, 'd5', open_bid, 100)
        d25 = self.get_ma_key(rate, 'd25', open_bid, 100)
        d75 = self.get_ma_key(rate, 'd75', open_bid, 200)

        # 流れの方向をキーにする
        key_trend = 'TRE:{}'.format(self.get_order_type(rates, open_bid).value)

        # キャンドル
        key_candle = self.get_key_candle(rates)

        return ':'.join(x for x in [d5, d25, d75, key_trend, key_candle] if x)

    def get_ma_key(self, rate, key, open_bid, ma_base_tick):
        diff_tick = ((open_bid - getattr(rate.ma, key)) / rate.tick)
        return 'MA:{}:{}'.format(key, get_tick_category(diff_tick, ma_base_tick))

    def get_key_candle(self, rates):
        c = len(rates)
        prev_rates = rates[c - self.depth:c]
        assert len(prev_rates) == self.depth, (len(prev_rates), self.depth)
        prev_rate = MultiCandles(prev_rates, Granularity.UNKNOWN)
        key_candle = 'CANDLE:{}'.format(prev_rate.get_candle_type(self.base_tick))
        return key_candle

    def get_order_type(self, prev_rates, open_bid):
        """
        注文方向を決定
        :param prev_rates: list of Rate
        :param open_bid: float
        :rtype : OrderType
        """
        if len(prev_rates) < 5:
            return OrderType.WAIT

        for rate in list(reversed(prev_rates[len(prev_rates) - 4: len(prev_rates)])):
            if rate.ma and rate.ma.d25:
                d25_diff_tick = int((open_bid - rate.ma.d25) / rate.tick)
                # 上げ相場
                if d25_diff_tick > self.up_down_base_tick:
                    return OrderType.BUY
                # 下げ相場
                if d25_diff_tick <= self.up_down_base_tick * -1:
                    return OrderType.SELL
        return OrderType.WAIT