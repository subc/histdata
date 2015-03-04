# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import random
import datetime
import django
from django.utils.functional import cached_property
from enum import Enum
import numpy
import time
import ujson
import requests
from module.genetic.models.case1 import LogicPatternCase1, AiBaseCase1
from module.genetic.models.history import GeneticHistory
from module.genetic.models.parameter import OrderType
from module.rate.models import CandleEurUsdH1Rate, CandleEurUsdDRate
from module.rate.models.eur import EurUsdMA
from utils.command import CustomBaseCommand
import copy
import multiprocessing as mp
from django.db import connection, connections
from utils.timeit import timeit
from django.core.cache import cache
from line_profiler import LineProfiler
from module.ai.models import AI1EurUsd as AI
from module.ai.models import AI2EurUsd as AI


@timeit
def benchmark(ai):
    print "start benchmark"
    candles = cache.get('candles')
    market = Market(ai.generation)

    for c in candles:
        if c.ma:
            print c.ma, c.ma.h1, c.ma.d75
        else:
            print "N/A c.ma"

    loop(ai, candles, market)

    # 確定処理
    rate = candles[-1]
    ai.update_market(market, rate)
    print('[ID:{}]SCORE:{} OPEN-SCORE:{} ポジション数:{} TRADE-COUNT:{}'.format(ai.generation,
                                                                  market.profit_summary(rate),
                                                                  market.current_profit(rate),
                                                                  len(market.open_positions),
                                                                  len(market.positions)))
    print('SCORE-MAX:{} SCORE-MIN:{}'.format(market.profit_max, market.profit_min))
    return ai


def loop(ai, candles, market):
    prev_rates = []
    for rate in candles:
        # 購入判断(prev rateに未来データを投入しないこと！！)
        market = ai.order(market, prev_rates, rate.open_bid, rate.start_at)

        # 決済
        market.payment(rate)

        # 過去のレートを更新
        prev_rates.append(rate)


class Command(CustomBaseCommand):
    suffix = None

    def handle(self, *args, **options):
        # キャンドルデータをキャッシュに設置
        candles = CandleEurUsdH1Rate.get_test_data()
        ma = EurUsdMA.get_all()
        mad = {m.start_at: m for m in ma}
        for candle in candles:
            candle.set_ma(mad.get(candle.start_at))
        cache.set('candles', candles, timeout=7200000)

        while True:
            self.run()

    def run(self):
        # 初期AI集団生成
        self.suffix = ':{}'.format(datetime.datetime.now())
        generation = 0
        size = 20  # 集団サイズ
        ai_mother = AI(AiBaseCase1, self.suffix, generation)
        ai_group = ai_mother.initial_create(20)
        proc = 8  # 並列処理数 コア数以上にしても無駄

        # 遺伝的アルゴリズムで進化させる
        while generation <= 100:
            # 評価
            generation += 1
            [ai.normalization() for ai in ai_group]

            pool = mp.Pool(proc)
            ai_group = pool.map(benchmark, ai_group)
            max_profit = max([ai.profit for ai in ai_group])
            history_write(ai_group)

            # 詰み回避
            trade_count = numpy.average([len(ai.market.positions) for ai in ai_group])
            if trade_count < 2000:
                print "取引平均回数が2000を下回ったので自殺:count:{}".format(trade_count)
                generation += 100000
            # 最高値制限
            if generation >= 10 and max_profit < 0:
                generation += 100000
            if generation >= 20 and max_profit < 100 * 10000:
                generation += 100000
            if generation >= 30 and max_profit < 150 * 10000:
                generation += 100000
            if generation >= 40 and max_profit < 200 * 10000:
                generation += 100000
            if generation >= 60 and max_profit < 250 * 10000:
                generation += 100000
            if generation >= 80 and max_profit < 300 * 10000:
                generation += 100000

            # 選択と交叉
            assert(type(ai_group[0]) == AI)
            ai_group = self.cross_over(size, ai_group)

            # normalization
            for ai in ai_group:
                ai.normalization()

            print '第{}世代 完了![score:{}]'.format(ai_group[0].generation, max_profit)

            # pool内のワーカープロセスを停止する
            pool.close()

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
        child_a = AI(child_a_dict, self.suffix, generation)
        child_b = AI(child_b_dict, self.suffix, generation)
        return [child_a, child_b]

    def _cross_value(self, value_a, value_b, _max, _min):
        """
        値を混ぜて、それぞれの遺伝子を持った値を返却
        :param value_a: int or list
        :param value_b: int or list
        :return: int or list
        """
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
        raise ValueError


class Market(object):
    positions = []
    open_positions = []
    profit_max = 0
    profit_min = 0
    profit_result = 0  # 最終利益
    close_profit = 0  # 確定した利益
    generation = 0
    calc_draw_down = False  # ドローダウンを計算するか(Trueで重くなる)
    start_at = None
    end_at = None

    def __init__(self, generation, calc_draw_down=False):
        self.positions = []
        self.generation = generation
        self.calc_draw_down = calc_draw_down

    def order(self, open_bid, order, start_at):
        """
        発注
        :param open_bid: float
        :param order: MarketOrder
        :param start_at: datetime
        """
        position = Position.open(start_at, open_bid, order.is_buy, limit_rate=order.limit_bid,
                                 stop_limit_rate=order.stop_limit_bid)
        # print 'OPEN![{}]:{}:{}:利確:{} 損切り:{}'.format(rate.start_at, order.is_buy, rate.open_bid, order.limit_bid, order.stop_limit_bid)
        self.open_positions.append(position)

    def payment(self, rate):
        """
        ポジションを精算する
        """
        # マーケット日時更新
        if self.start_at is None:
            self.start_at = rate.start_at
        self.end_at = rate.start_at

        # ドローダウン調査(重い)
        if self.calc_draw_down and random.randint(1, 10) == 1:
            self.record_profit(rate)
        for position in self.open_positions:
            if position.is_buy:
                # 損切り
                if rate.low_bid <= position.stop_limit_rate:
                    self._close(rate.start_at, position.stop_limit_rate, position)
                    continue
                # 利益確定
                if rate.high_bid >= position.limit_rate:
                    self._close(rate.start_at, position.limit_rate, position)
                    continue
            else:
                # 損切り
                if rate.high_bid >= position.stop_limit_rate:
                    self._close(rate.start_at, position.stop_limit_rate, position)
                    continue
                # 利益確定
                if rate.low_bid <= position.limit_rate:
                    self._close(rate.start_at, position.limit_rate, position)
                    continue

    def _close(self, start_at, rate, position):
        profit = position.close(start_at, rate)
        self.close_profit += profit
        self.positions.append(position)
        self.open_positions.remove(position)

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
        for position in self.open_positions:
            if position.is_open:
                r += position.get_current_profit(rate)
        return r

    def profit(self):
        """
        確定利益
        :rtype : int
        """
        return self.close_profit

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
    profit = None
    cost = 50

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
        self.profit = self.get_profit()
        # print 'CLOSE![{}] :open:{} close:{} 利益:¥{}'.format(end_at, self.open_rate, self.close_rate, self.get_profit())
        return self.profit


def _tick_to_yen(tick):
    """
    1tickを円に変換する
    :param tick: float
    :rtype : int
    """
    return int(tick * 10000 * 120)


def history_write(ai_group):
    """
    HTTP通信で書き込む
    """
    url_base = 'http://{}/genetic/history/'
    payload = ujson.dumps({
        'ai_group': [ai.to_dict() for ai in ai_group],
    })
    response = requests_post_api(url_base, payload=payload)
    assert response.status_code == 200, response.text


def requests_post_api(url_base, payload=None):
    TEST_HOST = '127.0.0.1:8000'
    url = url_base.format(TEST_HOST)
    payload = {'data': payload}
    requests.adapters.DEFAULT_RETRIES = 100
    response = requests.post(url, data=payload)
    print 'URL SUCCESS: {}'.format(url)
    return response


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
