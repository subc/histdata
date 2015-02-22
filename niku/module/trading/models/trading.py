# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import random


class TradingManager(object):
    POSITION_LIMIT = 10

    def __init__(self):
        from apps.parse.views import read_csv
        self.csv_data = read_csv()
        self.current_rate = None  # 現在の最新レート値
        self._index = 0
        self.positions = []

    def get_rate(self):
        """
        最新のレートを取得する。
        :rtype : boole
        """
        try:
            self.current_rate = self.generator()
            self._index += 1
        except IndexError:
            return False
        return True

    def sell(self):
        """
        既存ポジションを処理する
        :rtype : Position
        """
        for position in self.positions:
            if not position.is_open:
                continue

            profit = position.get_current_profit(self.current_rate)

            if profit >= 15000:
                position.close(self.current_rate)
                return position


            # 損失出てたら必ず処理
            # if profit < 0:
            #     position.close(self.current_rate)
            #     return position

            # 利益出てたら1/5の確率で処理
            # if random.randint(1, 5) == 1 and profit > 0:
            #     position.close(self.current_rate)
            #     return position

    def buy(self):
        """
        新規にポジションを立てたらTrue
        :rtype : Position
        """
        # 制限以上立てていたら立てない(リスク制限)
        if len(self.open_positions) >= self.POSITION_LIMIT:
            return None

        # 1.135なら購入する。
        if self.current_rate.pt_open <= 1.135:
            position = Position.open(self.current_rate)
            self.positions.append(position)
            return position
        # # 20%の確率でランダムで購入する。
        # if random.randint(1, 100) == 1:
        #     position = Position.open(self.current_rate)
        #     self.positions.append(position)
        #     return position
        return None

    def generator(self):
        return self.csv_data[self._index]

    @property
    def current_profit(self):
        """
        ポジション利益を表示
        :rtype : int
        """
        r = 0
        for position in self.positions:
            if position.is_open:
                r += position.get_current_profit(self.current_rate)
        return r

    @property
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

    @property
    def profit_summary(self):
        """
        確定利益 + ポジション利益
        :rtype : int
        """
        return self.current_profit + self.profit

    @property
    def open_positions(self):
        """
        未決済のポジションの数
        :rtype : list of Position
        """
        return [x for x in self.positions if x.is_open]

    @property
    def close_positions(self):
        """
        決済済みのポジションの数
        :rtype : list of Position
        """
        return [x for x in self.positions if not x.is_open]


class Position(object):
    """
    購入した資産
    """
    open_rate = None
    close_rate = None

    @classmethod
    def open(cls, rate):
        """
        ポジションを作る
        :param rate: CandleModel
        """
        position = cls()
        position.open_rate = rate
        return position

    @property
    def is_open(self):
        """
        そのポジションが未決済ならTrue
        :rtype : bool
        """
        return not bool(self.close_rate)

    def get_current_profit(self, rate):
        """
        現在の利益を計算する（円）
        :param rate: CandleModel
        :rtype : int
        """
        profit = rate.pt_open - self.open_rate.pt_open
        return _tick_to_yen(profit)

    def get_profit(self):
        """
        確定済みの利益を返却(円)
        :rtype : int
        """
        if self.is_open:
            return 0
        profit = self.close_rate.pt_open - self.open_rate.pt_open
        return _tick_to_yen(profit)

    def close(self, rate):
        """
        ポジションをクローズする
        :param rate: CandleModel
        """
        self.close_rate = rate


def _tick_to_yen(tick):
    """
    1tickを円に変換する
    :param tick: float
    :rtype : int
    """
    return int(tick * 10000 * 120)
