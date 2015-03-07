# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


class Position(object):
    """
    購入した資産
    """
    currency_pair = None
    start_at = None
    end_at = None
    limit_end_at = None
    open_rate = None
    close_rate = None
    limit_rate = None
    stop_limit_rate = None
    is_buy = None
    profit = None
    cost = 50

    def __init__(self, currency_pair, start_at, open_rate, is_buy, limit_rate=None, stop_limit_rate=None, limit_end_at=None):
        self.currency_pair = currency_pair
        self.start_at = start_at
        self.open_rate = open_rate
        self.is_buy = is_buy
        self.limit_rate = limit_rate
        self.stop_limit_rate = stop_limit_rate
        self.limit_end_at = limit_end_at

    @classmethod
    def open(cls, currency_pair, start_at, open_rate, is_buy, limit_rate=None, stop_limit_rate=None, limit_end_at=None):
        """
        ポジションを作る
        :param open_rate: float
        :param is_buy: bool
        """
        return cls(currency_pair, start_at, open_rate, is_buy,
                   limit_rate=limit_rate,
                   stop_limit_rate=stop_limit_rate,
                   limit_end_at=limit_end_at)

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
        return self.tick_to_yen(profit) - self.cost

    def get_profit(self):
        """
        確定済みの利益を返却(円)
        :rtype : int
        """
        if self.is_open:
            return 0
        profit = self.close_rate - self.open_rate
        return self.tick_to_yen(profit) - self.cost

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
        result = 'WIN' if self.profit >0 else 'LOSE'
        # print '[{}]CLOSE![{}] :open:{} close:{} profit:{}'.format(result, end_at, self.open_rate, self.close_rate, self.get_profit())
        return self.profit

    def tick_to_yen(self, tick):
        return self.currency_pair.tick_to_yen(tick)