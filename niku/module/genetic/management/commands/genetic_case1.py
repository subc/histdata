# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from module.genetic.models.case1 import LogicPatternCase1, AiBaseCase1
from module.rate.models import CandleEurUsdH1Rate, CandleEurUsdDRate
from utils.command import CustomBaseCommand


class Command(CustomBaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        h1_candles = CandleEurUsdH1Rate.get_all()
        # h1_candles = CandleEurUsdDRate.get_all()
        prev_rate = None
        market = Market()
        p = 20
        ai = AI(AiBaseCase1, p)
        for rate in h1_candles:
            # 購入判断
            market = ai.order(market, prev_rate, rate)

            # 決済
            market.payment(rate)

            prev_rate = rate

        # 結果
        ai.update_market(market)
        self.echo('ただいまの利益:{}円 ポジション損益:{}円 ポジション数:{} 総取引回数:{}'.format(market.profit_summary(rate),
                                                                      market.current_profit(rate),
                                                                      len(market.open_positions),
                                                                      len(market.close_positions)))
        self.echo('最大利益:{}円 最小利益:{}円'.format(market.profit_max, market.profit_min))


class Market(object):
    positions = []
    profit_max = 0
    profit_min = 0

    def __init__(self):
        self.positions = []

    def order(self, rate, is_buy, order_rate, stop_order_rate):
        """
        発注
        """
        position = Position.open(rate.start_at, rate.open_bid, is_buy, limit_rate=order_rate,
                                 stop_limit_rate=stop_order_rate)
        print 'OPEN![{}]:{}:{}:利確:{} 損切り:{}'.format(rate.start_at, is_buy, rate.open_bid, order_rate, stop_order_rate)
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

    @property
    def open_positions(self):
        return [x for x in self.positions if x.is_open]

    @property
    def close_positions(self):
        return [x for x in self.positions if not x.is_open]


class AI(object):
    LIMIT_POSITION = 10
    market = None
    ai_dict = {}
    p = None

    def __init__(self, ai_dict, p):
        self.ai_dict = ai_dict
        self.p = p

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
        assert (len(order_ai_list) == 3)

        # 発注
        _o = order_ai_list
        trade_type = _o[0]
        if trade_type == 2:
            return market
        is_buy = True if trade_type == 3 else False
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

    def update_market(self, market):
        self.market = market


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
        print 'CLOSE![{}] :open:{} close:{} 利益:¥{}'.format(end_at, self.open_rate, self.close_rate, self.get_profit())


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

    # print p_high, p_low, p_close
    return p_high * 100 + p_low * 10 + p_close


def get_type_by_diff(_d, p):
    """
    :param _d: int
    """
    # print _d
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