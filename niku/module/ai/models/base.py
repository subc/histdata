# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import copy
import random

from module.genetic.models.parameter import OrderType
from .market_order import MarketOrder, OrderAI
from module.currency import EurUsdMixin
from module.rate.models.base import MultiCandles


class AIInterFace(object):
    LIMIT_POSITION = 10
    market = None
    generation = None
    ai_dict = {}

    def __init__(self, ai_dict, suffix, generation):
        self.ai_dict = ai_dict
        self.name = self.__class__.__name__ + suffix
        self.generation = generation
        self.normalization()
        self._dispatch()

    @classmethod
    def get_ai(cls, history):
        """
        AIのdictからAIを生成して返却
        :param : AI
        """
        raise NotImplementedError

    def _dispatch(self):
        pass

    def save(self):
        """
        AIを記録する
        """
        from module.genetic.models import GeneticHistory
        GeneticHistory.record_history(self)

    def order(self, market, rates):
        """
        条件に沿って注文する
        :param market: Market
        :param rates: list of Rate
        :rtype market: Market
        """
        if not rates:
            return market

        # 既にポジション持ち過ぎ
        if len(market.open_positions) >= self.LIMIT_POSITION:
            return market
        order_ai = self.get_order_ai(market, rates)
        if not order_ai:
            return market

        if order_ai.order_type != OrderType.WAIT:
            market.order(rates[-1], MarketOrder(rates[-1], order_ai))
        return market

    def get_order_ai(self, market, rates):
        """
        :param market: Market
        :param rates: list of Rate
        :rtype : OrderAI
        """
        raise NotImplemented

    @classmethod
    def market_order(cls, market, rate, order_ai):
        """
        :param market: Market
        :param rate: Rate
        :param order_ai: OrderAI
        :rtype : Market
        """
        market.order(rate, MarketOrder(rate, order_ai))
        return market

    def update_market(self, market, rate):
        market.profit_result = market.profit_summary(rate)
        self._profit = market.profit_summary(rate)
        self._profit_max = market.profit_max
        self._profit_min = market.profit_min
        self.market = market

    def initial_create(self, num):
        """
        遺伝的アルゴリズム
        初期集団を生成
        :param num : int
        """
        return [copy.deepcopy(self).set_start_data() for x in xrange(num)]
        # return [copy.deepcopy(self) for x in xrange(num)]

    def increment_generation(self):
        """
        世代を1世代増やす
        """
        self.generation += 1
        return self

    def to_dict(self):
        return {
            'NAME': self.name,
            'GENERATION': self.generation,
            'PROFIT': self.profit,
            'PROFIT_MAX': self.profit_max,
            'PROFIT_MIN': self.profit_min,
            'AI_LOGIC': self._ai_to_dict(),
            'MARKET': self.market.to_dict(),
        }

    def _ai_to_dict(self):
        result_dict = {}
        for key in self.ai_dict:
            v = self.ai_dict[key]
            if type(v) == list:
                result_dict[key] = [self._value_to_dict(_v) for _v in v]
            else:
                result_dict[key] = self._value_to_dict(v)
        return result_dict

    def _value_to_dict(self, value):
        if type(value) == OrderType:
            return value.value
        return value

    def normalization(self):
        """
        過剰最適化するAIの進化に制限を儲ける
        利確, 損切り 800pip先とかを禁止
        """
        raise NotImplementedError

    def score(self, correct_value):
        return self.market.profit_result - correct_value

    @property
    def base_tick(self):
        return self.ai_dict.get('base_tick')

    @property
    def profit(self):
        return self._profit

    @property
    def profit_max(self):
        return self._profit_max

    @property
    def profit_min(self):
        return self._profit_min


class AI1EurUsd(EurUsdMixin, AIInterFace):
    # 進化乱数
    MUTATION_MAX = 60
    MUTATION_MIN = 10

    # 値の制限
    LIMIT_TICK = 60
    LIMIT_LOWER_TICK = 15
    LIMIT_BASE_HIGHER_TICK = 60
    LIMIT_BASE_LOWER_TICK = 10

    def normalization(self):
        """
        過剰最適化するAIの進化に制限を儲ける
        利確, 損切り 800pip先とかを禁止
        """
        ai = copy.deepcopy(self.ai_dict)
        for key in ai:
            if key == 'base_tick':
                if ai[key] <= self.LIMIT_BASE_LOWER_TICK:
                    ai[key] = self.LIMIT_BASE_LOWER_TICK
                if ai[key] >= self.LIMIT_BASE_HIGHER_TICK:
                    ai[key] = self.LIMIT_BASE_HIGHER_TICK
                continue
            # 13は必ずWAIT扱い
            if key == 13:
                ai[key] = [OrderType.WAIT, 0, 0]
            for index in [1, 2]:
                if ai[key][index] >= self.LIMIT_TICK:
                    ai[key][index] = self.LIMIT_TICK
                if ai[key][index] <= self.LIMIT_LOWER_TICK:
                    ai[key][index] = self.LIMIT_LOWER_TICK
        self.ai_dict = ai

    def set_start_data(self):
        """
        初期データを生成する
        """
        # tick 20%
        if random.randint(1, 100) <= 20:
            self.ai_dict['base_tick'] += random.randint(-2, 2)
        # 各パラメータは3%の確率で変異
        for key in self.ai_dict:
            if key == 'base_tick':
                continue
            value = self.ai_dict[key]
            if type(value) != list:
                continue
            for index in range(len(value)):
                self.ai_dict[key][0] = OrderType(random.randint(1, 3) - 2)
        self.normalization()
        return self

    def get_order_ai(self, market, rates):
        """
        条件に沿って注文する
        :param market: Market
        :param rates: list of Rate
        :rtype market: Market
        """
        if len(rates) < 3:
            return None
        prev_rate = rates[-2]

        # 前回のレートから型を探す
        candle_type_id = prev_rate.get_candle_type(self.base_tick)
        order_type, limit, stop_limit = self.ai_dict.get(candle_type_id)
        return OrderAI(order_type, limit, stop_limit)

    @classmethod
    def get_ai(cls, history):
        """
        AIのdictからAIを生成して返却
        :param : AI
        """
        ai = {}
        for key in history.ai:
            if key == 'base_tick':
                ai[key] = history.ai[key]
                continue
            if type(history.ai[key]) == list:
                l = history.ai[key]
                ai[key] = [OrderType(l[0]), l[1], l[2]]
                continue
            raise ValueError
        return cls(ai, history.name, history.generation)


class AI2EurUsd(AI1EurUsd):
    """
    数時間前にさかのぼってレートを参照する
    """
    # 進化乱数
    MUTATION_MAX = 60
    MUTATION_MIN = 10

    # 値の制限
    LIMIT_TICK = 60
    LIMIT_LOWER_TICK = 15
    LIMIT_BASE_HIGHER_TICK = 60
    LIMIT_BASE_LOWER_TICK = 10
    LIMIT_DEPTH = 48
    LIMIT_LOWER_DEPTH = 2

    def _dispatch(self):
        if 'depth' not in self.ai_dict:
            self.ai_dict['depth'] = 10

    def set_start_data(self):
        """
        初期データを生成する
        """
        # tick 20%
        if random.randint(1, 100) <= 20:
            self.ai_dict['base_tick'] += random.randint(-2, 2)
        # depth 100%
        self.ai_dict['depth'] = random.randint(self.LIMIT_LOWER_DEPTH, self.LIMIT_DEPTH)
        # 各パラメータは3%の確率で変異
        for key in self.ai_dict:
            if key == 'base_tick':
                continue
            value = self.ai_dict[key]
            if type(value) != list:
                continue
            for index in range(len(value)):
                self.ai_dict[key][0] = OrderType(random.randint(1, 3) - 2)
        self.normalization()
        return self

    def normalization(self):
        """
        過剰最適化するAIの進化に制限を儲ける
        利確, 損切り 800pip先とかを禁止
        """
        ai = copy.deepcopy(self.ai_dict)
        for key in ai:
            if key == 'base_tick':
                if ai[key] <= self.LIMIT_BASE_LOWER_TICK:
                    ai[key] = self.LIMIT_BASE_LOWER_TICK
                if ai[key] >= self.LIMIT_BASE_HIGHER_TICK:
                    ai[key] = self.LIMIT_BASE_HIGHER_TICK
                continue
            if key == 'depth':
                if self.LIMIT_LOWER_DEPTH > ai['depth']:
                    ai['depth'] = self.LIMIT_LOWER_DEPTH
                if self.LIMIT_DEPTH < ai['depth']:
                    ai['depth'] = self.LIMIT_DEPTH
                continue
            # 13は必ずWAIT扱い
            if key == 13:
                ai[key] = [OrderType.WAIT, 0, 0]
            for index in [1, 2]:
                if ai[key][index] >= self.LIMIT_TICK:
                    ai[key][index] = self.LIMIT_TICK
                if ai[key][index] <= self.LIMIT_LOWER_TICK:
                    ai[key][index] = self.LIMIT_LOWER_TICK
        self.ai_dict = ai

    def get_order_ai(self, market, rates):
        """
        条件に沿って注文する
        :param market: Market
        :param rates: list of Rate
        :rtype market: Market
        """
        if len(rates) < self.depth:
            return None
        c = len(rates)
        prev_rates = rates[c - self.depth:c]
        assert len(prev_rates) == self.depth, (len(prev_rates), self.depth)
        prev_rate = MultiCandles(prev_rates)

        # 前回のレートから型を探す
        candle_type_id = prev_rate.get_candle_type(self.base_tick)
        order_type, limit, stop_limit = self.ai_dict.get(candle_type_id)
        return OrderAI(order_type, limit, stop_limit)

    @property
    def depth(self):
        return self.ai_dict['depth']