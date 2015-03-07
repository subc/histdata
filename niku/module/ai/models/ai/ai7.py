# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
import random
from ..base import AI6EurUsd, get_range_rates, get_tick_category, convert_rate
from ..base import MultiCandles
from module.genetic.models.parameter import OrderType
from module.rate import Granularity


class AI7EurUsd(AI6EurUsd):
    """
    DrawDownを基準にした動作を行う
    """
    ai_id = 7

    def score(self, correct_value):
        """
        性能値を返却
        グループ中の下位5個の性能平均をスコアとする

        correct_valueは補正値だけど、このAIは使わない
        :param correct_value: float
        :rtype : int
        """
        return min(self.market.monthly_profit_group) - correct_value


class AI8EurUsd(AI7EurUsd):
    """
    DrawDownを基準にした動作を行う
    ver7からパラメータ調整版
    """
    ai_id = 8
    MUTATION_MAX = 60
    MUTATION_MIN = 10

    def _dispatch(self):
        if 'base_tick' not in self.ai_dict:
            self.ai_dict['base_tick'] = 20
        if 'depth' not in self.ai_dict:
            self.ai_dict['depth'] = 24

        # AI7 横横のときの売買基準
        if 'yokoyoko_base_tcik' not in self.ai_dict:
            self.ai_dict['yokoyoko_base_tcik'] = 20

        # AI7 上げ下げ相場の判断基準
        if 'up_down_base_tick' not in self.ai_dict:
            self.ai_dict['up_down_base_tick'] = 70

    def get_order_ai(self, market, prev_rates, open_bid, start_at):
        """
        条件に沿って注文する
        :param market: Market
        :param prev_rates: list of Rate
        :param open_bid: float
        :param start_at: datetime
        :rtype market: Market
        """
        rates = convert_rate(prev_rates, self.RATE_SPAN)

        if not rates:
            return None

        if len(rates) - 1 < self.depth:
            return None

        rate_type = self.get_ratetype(open_bid, rates, start_at)

        # rateがNoneのとき注文しない
        if rate_type is None:
            return None

        if rate_type in self.ai_dict:
            order_type, limit, stop_limit = self.ai_dict.get(rate_type)
        else:
            # AIがない場合はデフォルトデータをロード
            order_type = self.get_order_type(prev_rates, open_bid)
            self.ai_dict[rate_type] = [order_type, random.randint(15, 50), random.randint(30, 50)]
            order_type, limit, stop_limit = self.ai_dict.get(rate_type)
        from module.ai import OrderAI
        return OrderAI(order_type, limit, stop_limit)

    def get_order_type(self, prev_rates, open_bid):
        """
        注文方向を決定
        :param prev_rates: list of Rate
        :param open_bid: float
        :rtype : OrderType
        """
        if len(prev_rates) < 5:
            return OrderType.WAIT

        for rate in list(reversed(prev_rates[len(prev_rates) - 4: len(prev_rates)])):
            if rate.ma and rate.ma.d25:
                d25_diff_tick = int((open_bid - rate.ma.d25) / rate.tick)
                # 上げ相場
                if d25_diff_tick > self.up_down_base_tick:
                    return OrderType.BUY
                # 下げ相場
                if d25_diff_tick <= self.up_down_base_tick * -1:
                    return OrderType.SELL
        return OrderType.WAIT

    def get_ratetype(self, open_bid, rates, start_at):
        rate = rates[-1]
        if rate is None or rate.ma is None or rate.ma.h24 is None:
            return None

        # 横横検知
        y_key = None
        order_type = self.get_order_type(rates, open_bid)
        diff_tick = int((open_bid - rate.ma.h24) / rate.tick)
        if order_type == OrderType.BUY:
            # 上げ相場
            # 24時間以内の費用平均よりも、Npip下回っていること
            h24_category = get_tick_category(diff_tick, self.yokoyoko_base_tcik)
            if h24_category <= 0:
                y_key = 'Y-BUY:{}'.format(h24_category)
        elif order_type == OrderType.SELL:
            # 下げ相場
            # 24時間以内の費用平均よりも、Npip上回っていること
            h24_category = get_tick_category(diff_tick, self.yokoyoko_base_tcik)
            if h24_category >= 1:
                y_key = 'Y-SELL:{}'.format(h24_category)

        # key_ma_diffの生成
        prev_rate = rate
        error_range = datetime.timedelta(hours=24)   # 許容する後方誤差
        error_range2 = datetime.timedelta(hours=48)   # 許容する後方誤差
        rate24h_ago = get_range_rates(rates, start_at - datetime.timedelta(days=1), error_range)
        rate96h_ago = get_range_rates(rates, start_at - datetime.timedelta(days=4), error_range2)
        if rate24h_ago and rate24h_ago.ma and rate24h_ago.ma.d5:
            pass
        else:
            return None

        if rate96h_ago and rate96h_ago.ma and rate96h_ago.ma.d5:
            pass
        else:
            return None

        if rate24h_ago and rate96h_ago and prev_rate.ma and prev_rate.ma.d5:
            key2 = get_tick_category(rate24h_ago.ma.d5 - open_bid, self.base_tick)
            key3 = get_tick_category(rate96h_ago.ma.d5 - open_bid, self.base_tick)
            key_ma_diff = 'MA:{}:{}'.format(key2, key3)
        else:
            return None

        # key_candleの生成
        c = len(rates)
        prev_rates = rates[c - self.depth:c]
        assert len(prev_rates) == self.depth, (len(prev_rates), self.depth)
        prev_rate = MultiCandles(prev_rates, Granularity.UNKNOWN)
        key_candle = 'CANDLE:{}'.format(prev_rate.get_candle_type(self.base_tick))
        if y_key:
            return ':'.join([y_key, key_ma_diff, key_candle])
        else:
            return ':'.join([key_ma_diff, key_candle])

    @property
    def yokoyoko_base_tcik(self):
        return self.ai_dict['yokoyoko_base_tcik']

    @property
    def up_down_base_tick(self):
        return self.ai_dict['up_down_base_tick']