# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import random
import datetime
from enum import Enum
import numpy
from module.genetic.models.case1 import LogicPatternCase1, AiBaseCase1
from module.genetic.models.history import GeneticHistory
from module.genetic.models.parameter import OrderType
from module.rate.models import CandleEurUsdH1Rate, CandleEurUsdDRate
from utils.command import CustomBaseCommand
import copy
import multiprocessing as mp
from django.db import connection


class Command(CustomBaseCommand):
    AI_NAME = None

    def handle(self, *args, **options):
        self.init()
        self.run()

    def init(self):
        self.AI_NAME = 'AI_case1_{}'.format(datetime.datetime.now())

    def run(self):
        # h1_candles = CandleEurUsdH1Rate.get_all()

        # 初期AI集団生成
        generation = 0
        size = 20  # 初期集団サイズ
        selection = 4  # 選択するサイズ
        ai_mother = AI(AiBaseCase1, self.AI_NAME, generation)
        ai_group = ai_mother.initial_create(3)
        proc = 8    # 8並列とする

        # 遺伝的アルゴリズムで進化させる
        while True:
            # 評価
            generation += 1
            pool = mp.Pool(proc)
            callback = pool.map(benchmark, ai_group)

            # 選択
            ai_group = self.selection(callback, selection)

            # 交叉
            ai_group = self.cross_over(ai_group, size)

            # 突然変異
            for ai in ai_group:
                ai.mutation()
            print '第{}世代 完了!'.format(ai_group[0].generation)

    def selection(self, ai_group, selection):
        """
        遺伝的アルゴリズム
        選別する
        :param ai_group: list of AI
        :param selection: int
        :rtype : list of AI
        """
        r = []
        ai_group = sorted(ai_group, key=lambda x: x.score, reverse=True)
        # ランキング方式 1位が2体で2,3位が1体
        r.append(copy.deepcopy(ai_group[0]))
        r.append(copy.deepcopy(ai_group[0]))
        r.append(copy.deepcopy(ai_group[1]))
        r.append(copy.deepcopy(ai_group[2]))
        assert(len(r) == selection)
        return r

    def cross_over(self, ai_group, size):
        """
        遺伝的アルゴリズム
        交叉 配合する

        t = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        zip(t[::2], t[1::2])
        [('a', 'b'), ('c', 'd'), ('e', 'f'), ('g', 'h')]
        """
        # 偶数個に親の数をそろえる
        if len(ai_group) % 2:
            ai_group.append(ai_group[0])

        # pairを生成
        ai_pair = zip(ai_group[::2], ai_group[1::2])

        # 交叉する
        next_ai_group = []
        for ai_a, ai_b in ai_pair:
            next_ai_group += self._cross(ai_a, ai_b)
        next_ai_group += [ai.incr_generation() for ai in ai_group]  # 優秀な親を残す
        random.shuffle(next_ai_group)

        # 数が足りるまで複製
        while len(next_ai_group) < size:
            mutant = copy.deepcopy(next_ai_group)
            next_ai_group += [x.mutation() for x in mutant]
        return next_ai_group[:size]

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
            _a, _b = self._cross_value(_value_a, _value_b)
            child_a_dict[key] = _a
            child_b_dict[key] = _b

        # 子を生成
        child_a = AI(child_a_dict, self.AI_NAME, generation)
        child_b = AI(child_b_dict, self.AI_NAME, generation)
        return [child_a, child_b]

    def _cross_value(self, value_a, value_b):
        """
        値を混ぜて、それぞれの遺伝子を持った値を返却
        :param value_a: int or list
        :param value_b: int or list
        :return: int or list
        """
        if type(value_a) == type(value_b) == int:
            # 値の交換(一様交叉)
            if random.randint(1, 3) == 1:
                if random.randint(1, 2) == 1:
                    return value_a, value_b
                else:
                    return value_a, value_b
            # 値が混ざる(一点交叉)
            if random.randint(1, 3) == 1:
                if random.randint(1, 2) == 1:
                    return value_a, value_a
                else:
                    return value_b, value_b
            # 値の強化
            if random.randint(1, 3) == 1:
                summary = sum([value_a, value_b])
                return summary, summary

            # 値の平均
            average = int(numpy.average([value_a, value_b]))
            return average, average

        if type(value_a) == type(value_b) == list:
            list_a = []
            list_b = []
            _value_a = copy.deepcopy(value_a)
            _value_b = copy.deepcopy(value_b)
            for index in range(len(_value_a)):
                _a, _b = self._cross_value(_value_a[index], _value_b[index])
                list_a.append(_a)
                list_b.append(_b)
            return list_a, list_b

        if type(value_a) == type(value_b) == OrderType:
            return OrderType.cross_over(value_a, value_b)

        raise ValueError


def benchmark(ai):
    print "start benchmark"
    prev_rate = None
    market = Market()
    candles = CandleEurUsdH1Rate.get_all()

    for rate in candles:

        # 購入判断
        market = ai.order(market, prev_rate, rate)

        # 決済
        market.payment(rate)

        prev_rate = rate

    # 確定処理
    ai.update_market(market, rate)
    ai.save()
    print('ただいまの利益:{}円 ポジション損益:{}円 ポジション数:{} 総取引回数:{}'.format(market.profit_summary(rate),
                                                                  market.current_profit(rate),
                                                                  len(market.open_positions),
                                                                  len(market.close_positions)))
    print('最大利益:{}円 最小利益:{}円'.format(market.profit_max, market.profit_min))

    # DBコネクションを閉じる
    connection.close()
    return ai


class Market(object):
    positions = []
    profit_max = 0
    profit_min = 0
    profit_result = 0  # 最終利益

    def __init__(self):
        self.positions = []

    def order(self, rate, is_buy, order_rate, stop_order_rate):
        """
        発注
        """
        position = Position.open(rate.start_at, rate.open_bid, is_buy, limit_rate=order_rate,
                                 stop_limit_rate=stop_order_rate)
        # print 'OPEN![{}]:{}:{}:利確:{} 損切り:{}'.format(rate.start_at, is_buy, rate.open_bid, order_rate, stop_order_rate)
        self.positions.append(position)

    def payment(self, rate):
        """
        ポジションを精算する
        """
        self.record_profit(rate)
        for position in self.open_positions:
            if position.is_buy:
                # 損切り
                if rate.low_bid <= position.stop_limit_rate:
                    position.close(rate.start_at, position.stop_limit_rate)
                    continue
                # 利益確定
                if rate.high_bid >= position.limit_rate:
                    position.close(rate.start_at, position.limit_rate)
                    continue
            else:
                # 損切り
                if rate.high_bid >= position.stop_limit_rate:
                    position.close(rate.start_at, position.stop_limit_rate)
                    continue
                # 利益確定
                if rate.low_bid <= position.limit_rate:
                    position.close(rate.start_at, position.limit_rate)
                    continue

    def record_profit(self, rate):
        """
        最大利益と最小利益を記録
        """
        profit_summary = self.profit_summary(rate)

        if self.profit_max < profit_summary:
            self.profit_max = profit_summary
        if profit_summary < self.profit_min:
            self.profit_min = profit_summary

    def current_profit(self, rate):
        """
        ポジション利益を表示
        :rtype : int
        """
        r = 0
        for position in self.positions:
            if position.is_open:
                r += position.get_current_profit(rate)
        return r

    def profit(self):
        """
        確定利益
        :rtype : int
        """
        r = 0
        for position in self.positions:
            if not position.is_open:
                r += position.get_profit()
        return r

    def profit_summary(self, rate):
        """
        確定利益 + ポジション利益
        :rtype : int
        """
        return self.current_profit(rate) + self.profit()

    def to_dict(self):
        return {
            'positions': [p.to_dict() for p in self.positions],
            'profit_max': self.profit_max,
            'profit_min': self.profit_min,
            'profit_result': self.profit_result,
        }

    @property
    def open_positions(self):
        return [x for x in self.positions if x.is_open]

    @property
    def close_positions(self):
        return [x for x in self.positions if not x.is_open]


class AI(object):
    LIMIT_POSITION = 10
    market = None
    generation = None
    ai_dict = {}

    def __init__(self, ai_dict, name, generation):
        self.ai_dict = ai_dict
        self.name = name
        self.generation = generation

    def save(self):
        """
        AIを記録する
        """
        GeneticHistory.record_history(self)

    def order(self, market, prev_rate, rate):
        """
        条件に沿って注文する
        :param market: Market
        :param prev_rate: CandleEurUsdH1Rate
        :param rate: CandleEurUsdH1Rate
        """
        if prev_rate is None:
            return market

        # 既にポジション持ち過ぎ
        if len(market.open_positions) >= self.LIMIT_POSITION:
            return market

        # 前回のレートから型を探す
        candle_type = get_type(prev_rate, self.p)
        candle_type_id = LogicPatternCase1.get(candle_type)
        order_ai_list = self.ai_dict.get(candle_type_id)
        assert (len(order_ai_list) == 3), order_ai_list

        # 発注
        _o = order_ai_list
        trade_type = _o[0]
        if trade_type == OrderType.WAIT:
            return market
        is_buy = True if trade_type == OrderType.BUY else False
        if is_buy:
            order_rate = rate.open_bid + rate.tick * _o[1]
            stop_order_rate = rate.open_bid - rate.tick * _o[2]
        else:
            order_rate = rate.open_bid - rate.tick * _o[1]
            stop_order_rate = rate.open_bid + rate.tick * _o[2]

        market.order(rate,
                     is_buy,
                     order_rate,
                     stop_order_rate)
        return market

    def update_market(self, market, rate):
        market.profit_result = market.profit_summary(rate)
        self.market = market

    def initial_create(self, num):
        """
        遺伝的アルゴリズム
        初期集団を生成
        """
        return [copy.deepcopy(self).mutation() for x in xrange(num)]

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

    def incr_generation(self):
        """
        世代を1世代増やす
        """
        self.generation += 1
        return self

    def to_dict(self):
        return {
            'AI_LOGIC': self.ai_to_dict(),
            'MARKET': self.market.to_dict(),
        }

    def ai_to_dict(self):
        result_dict = {}
        for key in self.ai_dict:
            value = self.ai_dict[key]
            if type(value) == list:
                result_dict[key] = [self.value_to_dict(_v) for _v in value]
            else:
                result_dict[key] = self.value_to_dict(value)
        return result_dict

    def value_to_dict(self, value):
        if type(value) == OrderType:
            return value.value
        return value

    @property
    def p(self):
        return self.ai_dict.get('base_tick')

    @property
    def score(self):
        return self.market.profit_result


class Position(object):
    """
    購入した資産
    """
    start_at = None
    end_at = None
    open_rate = None
    close_rate = None
    limit_rate = None
    stop_limit_rate = None
    is_buy = None
    cost = 100

    def __init__(self, start_at, open_rate, is_buy, limit_rate=None, stop_limit_rate=None):
        self.start_at = start_at
        self.open_rate = open_rate
        self.is_buy = is_buy
        self.limit_rate = limit_rate
        self.stop_limit_rate = stop_limit_rate

    @classmethod
    def open(cls, start_at, open_rate, is_buy, limit_rate=None, stop_limit_rate=None):
        """
        ポジションを作る
        :param open_rate: float
        :param is_buy: bool
        """
        return cls(start_at, open_rate, is_buy, limit_rate=limit_rate, stop_limit_rate=stop_limit_rate)

    @property
    def is_open(self):
        """
        そのポジションが未決済ならTrue
        :rtype : bool
        """
        return not bool(self.end_at)

    def to_dict(self):
        return {
            'start_at': str(self.start_at),
            'end_at': str(self.end_at),
            'open_rate': self.open_rate,
            'close_rate': self.close_rate,
            'limit_rate': self.limit_rate,
            'stop_limit_rate': self.stop_limit_rate,
            'is_buy': self.is_buy
        }

    def get_current_profit(self, rate):
        """
        現在の利益を計算する（円）
        :param rate: CandleModel
        :rtype : int
        """
        profit = rate.open_bid - self.open_rate
        return _tick_to_yen(profit) - self.cost

    def get_profit(self):
        """
        確定済みの利益を返却(円)
        :rtype : int
        """
        if self.is_open:
            return 0
        profit = self.close_rate - self.open_rate
        return _tick_to_yen(profit) - self.cost

    def close(self, end_at, rate_bid):
        """
        ポジションをクローズする
        :param end_at: datetime
        :param rate_bid: float
        """
        if not self.is_open:
            raise ValueError

        self.end_at = end_at
        self.close_rate = rate_bid
        # print 'CLOSE![{}] :open:{} close:{} 利益:¥{}'.format(end_at, self.open_rate, self.close_rate, self.get_profit())


def _tick_to_yen(tick):
    """
    1tickを円に変換する
    :param tick: float
    :rtype : int
    """
    return int(tick * 10000 * 120)


def get_type(rate, p):
    """
    :param rate: CandleEurUsdH1Rate
    :param p: int
    """
    tick = 0.0001
    p_high = get_type_by_diff((rate.high_bid - rate.open_bid) / tick, p)
    p_low = get_type_by_diff((rate.low_bid - rate.open_bid) / tick, p)
    p_close = get_type_by_diff(int((rate.close_bid - rate.open_bid) / tick), p)
    return p_high * 100 + p_low * 10 + p_close


def get_type_by_diff(_d, p):
    """
    :param _d: int
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