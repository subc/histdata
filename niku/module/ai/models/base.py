# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import copy
import random

from module.genetic.models.parameter import OrderType
from .market_order import MarketOrder, OrderAI
from module.currency import EurUsdMixin


class AIInterFace(object):
    LIMIT_POSITION = 10
    market = None
    generation = None
    ai_dict = {}

    def __init__(self, ai_dict, name, generation):
        self.ai_dict = ai_dict
        self.name = name
        self.generation = generation
        self.normalization()

    @classmethod
    def get_ai(cls, history):
        """
        AIのdictからAIを生成して返却
        :param : AI
        """
        raise NotImplementedError

    def save(self):
        """
        AIを記録する
        """
        from module.genetic.models import GeneticHistory
        GeneticHistory.record_history(self)

    def order(self, market, prev_rate, rate):
        """
        条件に沿って注文する
        :param market: Market
        :param rate: Rate
        :rtype market: Market
        """
        if prev_rate is None:
            return market

        # 既にポジション持ち過ぎ
        if len(market.open_positions) >= self.LIMIT_POSITION:
            return market
        order_ai = self.get_order_ai(market, rate, prev_rate)
        if order_ai.order_type != OrderType.WAIT:
            market.order(rate, MarketOrder(rate, order_ai))
        return market

    def get_order_ai(self, market, rate, prev_rate):
        """
        :param market: Market
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
        return [copy.deepcopy(self).mutation() for x in xrange(num)]

    def mutation(self):
        raise NotImplementedError

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

    @property
    def score(self):
        return self.market.profit_result


class AI1EurUsd(EurUsdMixin, AIInterFace):
    LIMIT_TICK = 60
    LIMIT_LOWER_TICK = 5
    LIMIT_BASE_HIGHER_TICK = 60
    LIMIT_BASE_LOWER_TICK = 15

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
            for index in [1, 2]:
                if ai[key][index] >= self.LIMIT_TICK:
                    ai[key][index] = self.LIMIT_TICK
                if ai[key][index] <= self.LIMIT_LOWER_TICK:
                    ai[key][index] = self.LIMIT_LOWER_TICK
        self.ai_dict = ai

    def mutation(self):
        """
        遺伝的アルゴリズム
        突然変異させる
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
                if random.randint(1, 100) <= 3:
                    if type(value[index]) == OrderType:
                        self.ai_dict[key][index] = OrderType.mutation(value[index])
                    else:
                        self.ai_dict[key][index] += random.randint(-10, 10)
        return self

    def get_order_ai(self, market, rate, prev_rate):
        """
        条件に沿って注文する
        :param market: Market
        :param rate: Rate
        :rtype market: Market
        """
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
