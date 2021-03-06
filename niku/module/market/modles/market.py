# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict
import random
from django.utils.functional import cached_property
from .position import Position


class Market(object):
    positions = []  # 閉じたポジション
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

    def order(self, currency_pair, open_bid, order, start_at):
        """
        発注
        :param currency_pair: CurrencyPair
        :param open_bid: float
        :param order: MarketOrder
        :param start_at: datetime
        """
        if order.is_buy:
            assert order.stop_limit_bid < open_bid < order.limit_bid
        else:
            assert order.limit_bid < open_bid < order.stop_limit_bid

        position = Position.open(currency_pair, start_at, open_bid, order.is_buy, limit_rate=order.limit_bid,
                                 stop_limit_rate=order.stop_limit_bid, limit_end_at=order.limit_end_at)
        # print 'OPEN![{}]:{}:{}:利確:{} 損切り:{}'.format(start_at, order.is_buy, open_bid, order.limit_bid, order.stop_limit_bid)
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
        if self.calc_draw_down:
            self.record_profit(rate)
        for position in self.open_positions:
            # ポジションの有効期限切れ
            if position.limit_end_at:
                if rate.start_at > position.limit_end_at:
                    _profit = self._close(rate.start_at, rate.open_bid, position)
                    assert position.start_at < position.end_at
                    if random.randint(1, 1000) == 1:
                        print 'TIME IS OVER[BUY:{}][PROFIT:{}] from:{} to:{} start:{} end:{}'.format(
                            position.is_buy,
                            _profit,
                            position.open_rate,
                            position.close_rate,
                            position.start_at,
                            position.end_at
                        )
                    continue

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
        return profit

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

    @cached_property
    def monthly_profit_group(self):
        """
        月毎の利益を返却
        :rtype : list of int
        """
        d = defaultdict(int)
        for position in self.positions:
            d['{}:{}'.format(position.start_at.year, position.start_at.month)] += position.get_profit()
        return d.values()