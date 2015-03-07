# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import copy
import random
import datetime
from module.genetic.models.parameter import OrderType


class GeneticMixin(object):
    def cross_over(self, size, ai_group):
        """
        遺伝的アルゴリズム
        交叉 配合する
        """
        # sizeは偶数であること
        if size % 2 != 0:
            raise ValueError

        # エリート主義(上位3名を残す)
        # elite_group = sorted(ai_group, key=lambda x: x.score(0), reverse=True)[:3]
        # elite_group = copy.deepcopy(elite_group)
        # elite_group = [ai.incr_generation() for ai in elite_group]

        # ルーレット選択方式で親を選択して交叉する
        next_ai_group = []
        while len(next_ai_group) != size:
            next_ai_group += self._cross(self.roulette_selection(ai_group),
                                         self.roulette_selection(ai_group))
        return next_ai_group

    def _cross(self, ai_a, ai_b):
        """
        2体の親を交叉して、子供を2体生成
        :param ai_a: AI
        :param ai_b: AI
        :return: list of AI
        """
        generation = ai_a.generation + 1
        child_a_dict = {}
        child_b_dict = {}
        for key in ai_a.ai_dict:
            _value_a = ai_a.ai_dict.get(key)
            _value_b = ai_b.ai_dict.get(key)
            _a, _b = self._cross_value(_value_a, _value_b, ai_a.MUTATION_MAX, ai_a.MUTATION_MIN)
            child_a_dict[key] = _a
            child_b_dict[key] = _b

        # 子を生成
        child_a = self.ai_class(child_a_dict, self.suffix, generation)
        child_b = self.ai_class(child_b_dict, self.suffix, generation)
        return [child_a, child_b]

    def _cross_value(self, value_a, value_b, _max, _min):
        """
        値を混ぜて、それぞれの遺伝子を持った値を返却
        :param value_a: int or list
        :param value_b: int or list
        :return: int or list
        """
        # int
        if type(value_a) == type(value_b) == int:
            if random.randint(1, 100) == 2:
                # 突然変異
                _v = random.randint(_min, _max)
                return _v, _v
            elif random.randint(1, 100) <= 85:
                # 2点交叉
                return cross_2point(value_a, value_b)
            else:
                # 何もしない
                return value_a, value_b

        # list
        if type(value_a) == type(value_b) == list:
            list_a = []
            list_b = []
            _value_a = copy.deepcopy(value_a)
            _value_b = copy.deepcopy(value_b)
            for index in range(len(_value_a)):
                _a, _b = self._cross_value(_value_a[index], _value_b[index], _max, _min)
                list_a.append(_a)
                list_b.append(_b)
            return list_a, list_b

        # dict
        if type(value_a) == type(value_b) == dict:
            dict_a = {}
            dict_b = {}
            _value_a = copy.deepcopy(value_a)
            _value_b = copy.deepcopy(value_b)
            for key in _value_a:
                _a, _b = self._cross_value(_value_a[key], _value_b[key], _max, _min)
                dict_a[key] = _a
                dict_b[key] = _b
            return dict_a, dict_b

        # OrderType
        if type(value_a) == type(value_b) == OrderType:
            if random.randint(1, 100) == 2:
                # 突然変異
                return OrderType.mutation(value_b), OrderType.mutation(value_a)
            elif random.randint(1, 100) <= 85:
                # 交叉
                return OrderType.cross_over(value_a, value_b)
            else:
                # 何もしない
                return value_a, value_b

        # datetime
        if type(value_a) == type(value_b) == datetime.datetime:
            return value_a, value_b

        # どちらかがNone
        if value_a is None or value_b is None:
            if value_a is None:
                return value_b, value_b
            if value_b is None:
                return value_a, value_a

        raise ValueError, "{}[type:{}]:{}[type:{}]".format(value_a, type(value_a), value_b, type(value_b))

    def roulette_selection(self, ai_group):
        """
        遺伝的アルゴリズム
        ルーレット選択方式 スコアを重みとして選択
        :param ai_group: list of AI
        :rtype : AI
        """
        # スコアがマイナスのときは補正値を使う
        correct_value = min([ai.score(0) for ai in ai_group])
        if correct_value > 0:
            correct_value = 0

        total = sum([ai.score(correct_value) for ai in ai_group])
        r = random.randint(0, total)
        _total = 0
        for ai in ai_group:
            _total += ai.score(correct_value)
            if r <= _total:
                return ai
        raise ValueError


def cross_2point(a, b):
    """
    2点交叉
    :param a: int
    :param b: int
    """
    a = format(a, 'b')
    b = format(b, 'b')
    max_length = max([len(a), len(b)])
    if len(a) < max_length:
        a = '0' * (max_length - len(a)) + a
    if len(b) < max_length:
        b = '0' * (max_length - len(b)) + b
    point1 = random.randint(1, max_length)
    point2 = random.randint(1, max_length)
    point_max = max(point1, point2)
    point_min = min(point1, point2)
    a = a[:point_min] + b[point_min:point_max] + a[point_max:]
    b = b[:point_min] + a[point_min:point_max] + b[point_max:]
    return int(a, 2), int(b, 2)