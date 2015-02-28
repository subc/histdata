# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import random
import datetime
import django
from enum import Enum
import numpy
import time
import ujson
import requests
from module.genetic.models.case1 import LogicPatternCase1, AiBaseCase1
from module.genetic.models.history import GeneticHistory
from module.genetic.models.parameter import OrderType
from module.rate.models import CandleEurUsdH1Rate, CandleEurUsdDRate
from utils.command import CustomBaseCommand
import copy
import multiprocessing as mp
from django.db import connection, connections
from utils.timeit import timeit
from django.core.cache import cache
from line_profiler import LineProfiler
from module.ai.models import AI1EurUsd as AI


@timeit
def benchmark(ai):
    print "start benchmark"
    candles = cache.get('candles')
    market = Market()

    loop(ai, candles, market)

    # 確定処理
    rate = candles[-1]
    ai.update_market(market, rate)
    print('ただいまの利益:{}円 ポジション損益:{}円 ポジション数:{} 総取引回数:{}'.format(market.profit_summary(rate),
                                                                  market.current_profit(rate),
                                                                  len(market.open_positions),
                                                                  len(market.positions)))
    print('最大利益:{}円 最小利益:{}円'.format(market.profit_max, market.profit_min))
    return ai

@timeit
def loop(ai, candles, market):
    prev_rate = None
    # prf = LineProfiler() #インスタンスに複数の関数を与えても良い。
    for rate in candles:

        # prf.add_function(ai.order)
        # market = prf.runcall(ai.order, market, prev_rate, rate)
        #
        # prf.add_function(market.payment)
        # prf.runcall(market.payment, rate)
        # 購入判断
        market = ai.order(market, prev_rate, rate)

        # 決済
        market.payment(rate)

        prev_rate = rate
    # prf.print_stats()


class Command(CustomBaseCommand):
    AI_NAME = None

    def handle(self, *args, **options):
        self.init()
        self.run()

    def init(self):
        self.AI_NAME = 'AI_case1_{}'.format(datetime.datetime.now())

    def run(self):
        # h1_candles = CandleEurUsdH1Rate.get_all()
        # candles = CandleEurUsdH1Rate.get_test_data2()[:100]

        # 初期AI集団生成
        generation = 0
        size = 20  # 初期集団サイズ
        selection = 4  # 選択するサイズ
        ai_mother = AI(AiBaseCase1, self.AI_NAME, generation)
        ai_group = ai_mother.initial_create(20)
        proc = 1  # 8並列とする

        # 計算元データを計算
        candles = CandleEurUsdH1Rate.get_test_data2()
        cache.set('candles', candles, timeout=7200)

        # re_connection()

        # 遺伝的アルゴリズムで進化させる
        while generation < 100:
            # 評価
            generation += 1
            [ai.normalization() for ai in ai_group]
            pool = mp.Pool(proc)
            ai_group = pool.map(benchmark, ai_group)
            # django.db.close_old_connections()
            # GeneticHistory.bulk_create_by_ai(ai_group)
            history_write(ai_group)

            # 選択
            ai_group = self.selection(ai_group, selection)

            # 交叉
            next_ai_group = self.cross_over(ai_group, size)

            # 突然変異
            for ai in next_ai_group:
                ai.mutation()

            print '第{}世代 完了!'.format(ai_group[0].generation)

            # pool内のワーカープロセスを停止する
            pool.close()

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
                    return value_b, value_a
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


def re_connection():
    """
    wait_timeout対策
    バックグラウンドでループして動かすと、playerのshardはcommit_on_success外でコネクションが生きている可能性があるので
    カーソルを取り直すおまじないです
    """
    db_name = 'default'
    timeout = 36000
    con = connections[db_name].connection
    if con:
        cur = con.cursor()
    else:
        cur = connections[db_name].cursor()
    cur.execute('set session wait_timeout = {}'.format(timeout))
    # pass


class Market(object):
    positions = []
    open_positions = []
    profit_max = 0
    profit_min = 0
    profit_result = 0  # 最終利益

    def __init__(self):
        self.positions = []

    def order(self, rate, order):
        """
        発注
        :param rate: Rate
        :param order: MarketOrder
        """
        position = Position.open(rate.start_at, rate.open_bid, order.is_buy, limit_rate=order.limit_bid,
                                 stop_limit_rate=order.stop_limit_bid)
        # print 'OPEN![{}]:{}:{}:利確:{} 損切り:{}'.format(rate.start_at, is_buy, rate.open_bid, order_rate, stop_order_rate)
        self.open_positions.append(position)

    def payment(self, rate):
        """
        ポジションを精算する
        """
        # self.record_profit(rate)
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
        position.close(start_at, rate)
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
                r += position.profit
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
        self.profit = self.get_profit()
        # print 'CLOSE![{}] :open:{} close:{} 利益:¥{}'.format(end_at, self.open_rate, self.close_rate, self.get_profit())



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
    response = requests.post(url, data=payload)
    print 'URL SUCCESS: {}'.format(url)
    return response
