# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import copy
import random

from ..base import AIInterFace, get_tick_category, convert_rate
from ..mixin import DispatchMixin
from module.currency import UsdJpyMixin, GbpUsdMixin, AudUsdMixin
from module.genetic.models.parameter import OrderType
from module.rate import Granularity
from module.rate.models.base import MultiCandles


class AIUsdJpyBase(DispatchMixin, AIInterFace):
    MUTATION_MAX = 120
    MUTATION_MIN = 10
    RATE_SPAN = Granularity.H1

    def score(self, correct_value):
        """
        性能値を返却
        期間を通しての利益で計算する

        correct_valueは補正値だけど、このAIは使わない
        :param correct_value: float
        :rtype : int
        """
        return self.profit - correct_value

    def set_start_data(self):
        return self

    def get_order_ai(self, prev_rates, open_bid, start_at, is_production=False):
        """
        条件に沿って注文する
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

        rate_type = self.get_key(open_bid, rates, start_at)

        # rateがNoneのとき注文しない
        if rate_type is None:
            return None

        if rate_type in self.ai_dict:
            order_type, limit, stop_limit = self.ai_dict.get(rate_type)
        else:
            if is_production:
                print 'RANDOM WALK!!!', rate_type
                return None
            # AIがない場合はデフォルトデータをロード
            self.ai_dict[rate_type] = [OrderType.get_random(),
                                       random.randint(self.MUTATION_MIN, self.MUTATION_MAX),
                                       random.randint(self.MUTATION_MIN, self.MUTATION_MAX)]
            order_type, limit, stop_limit = self.ai_dict.get(rate_type)
        from module.ai import OrderAI
        return OrderAI(order_type, limit, stop_limit)

    def normalization(self):
        """
        過剰最適化するAIの進化に制限を儲ける
        利確, 損切り 800pip先とかを禁止
        """
        ai = copy.deepcopy(self.ai_dict)
        for key in ai:
            if type(ai[key]) == list:
                for index in [1, 2]:
                    ai[key][index] = self.adjust(ai[key][index])
                continue
            ai[key] = self.adjust(ai[key])
        self.ai_dict = ai

    def adjust(self, value):
        if self.MUTATION_MAX < value:
            return self.MUTATION_MAX
        if self.MUTATION_MIN > value:
            return self.MUTATION_MIN
        return value

    def get_key(self, open_bid, rates, start_at):
        raise NotImplementedError


class AI1001Base(AIUsdJpyBase):
    MUTATION_MAX = 120
    MUTATION_MIN = 10

    def get_key(self, open_bid, rates, start_at):
        rate = rates[-1]
        if rate is None or rate.ma is None or rate.ma.h24 is None:
            return None

        # MA
        d5 = self.get_ma_key(rate, 'd5', open_bid, 100)
        d25 = self.get_ma_key(rate, 'd25', open_bid, 100)
        d75 = self.get_ma_key(rate, 'd75', open_bid, 200)

        # 流れの方向をキーにする
        key_trend = 'TRE:{}'.format(self.get_order_type(rates, open_bid).value)

        # キャンドル
        key_candle = self.get_key_candle(rates)

        return ':'.join(x for x in [d5, d25, d75, key_trend, key_candle] if x)

    def get_ma_key(self, rate, key, open_bid, ma_base_tick):
        diff_tick = ((open_bid - getattr(rate.ma, key)) / rate.tick)
        return 'MA:{}:{}'.format(key, get_tick_category(diff_tick, ma_base_tick))

    def get_key_candle(self, rates):
        c = len(rates)
        prev_rates = rates[c - self.depth:c]
        assert len(prev_rates) == self.depth, (len(prev_rates), self.depth)
        prev_rate = MultiCandles(prev_rates, Granularity.UNKNOWN)
        key_candle = 'CANDLE:{}'.format(prev_rate.get_candle_type(self.base_tick))
        return key_candle

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


class AI2001Gbp(GbpUsdMixin, AI1001Base):
    ai_id = 2001
    MUTATION_MAX = 150
    MUTATION_MIN = 10
    pass


class AI3001Aud(AudUsdMixin, AI1001Base):
    ai_id = 3001
    MUTATION_MAX = 120
    MUTATION_MIN = 10
    pass


class AIHoriBase(AI1001Base):
    MUTATION_MAX = 120
    MUTATION_MIN = 10

    def get_key(self, open_bid, rates, start_at):
        rate = rates[-1]
        if rate is None or rate.ma is None:
            return None

        # 最高値からの乖離で取得
        key_hori_high_low_diff = rate.ma.key_category_d25

        # 水平でキー取得
        key_hori_diff = self.get_horizontal_diff_key(rate.ma, open_bid, rate.currency_pair)

        # MA
        d5 = self.get_ma_key(rate, 'd5', open_bid, 100)
        # d25 = self.get_ma_key(rate, 'd25', open_bid, 100)
        # d75 = self.get_ma_key(rate, 'd75', open_bid, 200)

        # 流れの方向をキーにする
        # key_trend = 'TRE:{}'.format(self.get_order_type(rates, open_bid).value)

        # キャンドル
        key_candle = self.get_key_candle(rates)

        return ':'.join(x for x in [key_hori_high_low_diff, key_hori_diff, key_candle, d5] if x)

    def get_horizontal_diff_key(self, ma, open_bid, pair):
        """
        現在レートと過去の最高値と安値の乖離
        :param ma: MovingAverageBase
        :param open_bid: float
        :param pair: CurrencyPair
        :return:
        """
        # d25水平で現在レートとの差を取得
        high_d25 = get_tick_category((ma.high_horizontal_d25 - open_bid) / pair.get_base_tick(), 50)
        low_d25 = get_tick_category((ma.low_horizontal_d25 - open_bid) / pair.get_base_tick(), 50)

        # d5水平で現在レートとの差を取得
        # high_d5 = get_tick_category((ma.high_horizontal_d5 - open_bid) / pair.get_base_tick(), 50)
        # low_d5 = get_tick_category((ma.low_horizontal_d5 - open_bid) / pair.get_base_tick(), 50)
        return 'HORI-DIFF:D25:{}:{}'.format(high_d25, low_d25)


class AIHoriUsdJpy1002(UsdJpyMixin, AIHoriBase):
    ai_id = 1002


class AIHoriGbpUsd2002(GbpUsdMixin, AIHoriBase):
    ai_id = 2002
    MUTATION_MAX = 150
    MUTATION_MIN = 10


class AIMultiCandleBase(AIHoriBase):
    def get_key(self, open_bid, rates, start_at):
        rate = rates[-1]
        if rate is None or rate.ma is None:
            return None

        # 最高値からの乖離で取得
        # key_hori_high_low_diff = rate.ma.key_category_d25

        # 水平でキー取得
        key_hori_diff = self.get_horizontal_diff_key(rate.ma, open_bid, rate.currency_pair)

        # MA
        # d5 = self.get_ma_key(rate, 'd5', open_bid, 100)
        # d25 = self.get_ma_key(rate, 'd25', open_bid, 100)
        # d75 = self.get_ma_key(rate, 'd75', open_bid, 200)

        # 流れの方向をキーにする
        # key_trend = 'TRE:{}'.format(self.get_order_type(rates, open_bid).value)

        # キャンドル
        # key_candle_h1 = self.get_key_candle_general(rates, 1, self.candle_h1_base_tick)
        key_candle_h4 = self.get_key_candle_general(rates, 4, self.candle_h4_base_tick)
        key_candle_h24 = self.get_key_candle_general(rates, 24, self.candle_h24_base_tick)
        # key_candle_h48 = self.get_key_candle_general(rates, 48, self.candle_h48_base_tick)
        # key_candle_h72 = self.get_key_candle_general(rates, 72, self.candle_h72_base_tick * 2)
        key_candle_h120 = self.get_key_candle_general(rates, 120, self.candle_h120_base_tick * 2)
        # key_candle_h240 = self.get_key_candle_general(rates, 240, self.candle_h240_base_tick * 2)
        key_candle_group = [key_candle_h4,
                            key_candle_h24,
                            key_candle_h120]

        if None in key_candle_group:
            return None
        key_candle = self.get_key_candle(rates)
        key_candle_plus = ':'.join(key_candle_group)

        return ':'.join(x for x in [key_hori_diff, key_candle, key_candle_plus] if x)

    def get_key_candle_general(self, rates, depth, base_tick):

        c = len(rates)
        prev_rates = rates[c - depth:c]
        if len(prev_rates) != depth:
            return None
        prev_rate = MultiCandles(prev_rates, Granularity.UNKNOWN)
        key_candle = 'CANDLE:{}'.format(prev_rate.get_candle_type(base_tick))
        return key_candle


class AIMultiCandleUsdJpy1003(UsdJpyMixin, AIMultiCandleBase):
    ai_id = 1003
    MUTATION_MAX = 80
    MUTATION_MIN = 10
