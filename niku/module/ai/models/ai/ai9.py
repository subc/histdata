# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
import random
from ..base import AI6EurUsd, get_range_rates, get_tick_category, convert_rate
from ..base import MultiCandles
from .ai7 import AI8EurUsd
from module.genetic.models.parameter import OrderType
from module.rate import Granularity


class AI9EurUsd(AI8EurUsd):
    """
    DrawDownを基準にした動作を行う
    """
    ai_id = 9
    MUTATION_MAX = 120
    MUTATION_MIN = 10

    def score(self, correct_value):
        """
        性能値を返却
        グループ中の下位5個の性能平均をスコアとする

        correct_valueは補正値だけど、このAIは使わない
        :param correct_value: float
        :rtype : int
        """
        return min(self.market.monthly_profit_group) - correct_value

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

        rate_type = self.get_ratetype(open_bid, rates, start_at)

        # rateがNoneのとき注文しない
        if rate_type is None:
            return None

        if rate_type in self.ai_dict:
            order_type, limit, stop_limit = self.ai_dict.get(rate_type)
        else:
            if is_production:
                print 'RANDOM WALK!!'
                return None
            # AIがない場合はデフォルトデータをロード
            self.ai_dict[rate_type] = [OrderType.get_random(), random.randint(20, 100), random.randint(20, 100)]
            order_type, limit, stop_limit = self.ai_dict.get(rate_type)
        from module.ai import OrderAI
        return OrderAI(order_type, limit, stop_limit)

    def get_ratetype(self, open_bid, rates, start_at):
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


class AI10EurUsd(AI9EurUsd):
    ai_id = 10
    MUTATION_MAX = 120
    MUTATION_MIN = 10

    def score(self, correct_value):
        """
        性能値を返却
        期間を通しての利益で計算する

        correct_valueは補正値だけど、このAIは使わない
        :param correct_value: float
        :rtype : int
        """
        return self.profit - correct_value


class AI11EurUsd(AI9EurUsd):
    ai_id = 11
    MUTATION_MAX = 80
    MUTATION_MIN = 12

    def score(self, correct_value):
        """
        性能値を返却
        期間を通しての利益で計算する

        correct_valueは補正値だけど、このAIは使わない
        :param correct_value: float
        :rtype : int
        """
        return self.profit - correct_value

    def get_ratetype(self, open_bid, rates, start_at):
        rate = rates[-1]
        if rate is None or rate.ma is None:
            return None

        # 最高値からの乖離で取得
        key_hori_high_low_diff = rate.ma.key_category

        # 水平でキー取得
        key_hori_diff = self.get_horizontal_diff_key(rate.ma, open_bid, rate.currency_pair)

        # MA
        # d75 = self.get_ma_key(rate, 'd75', open_bid, 200)

        # 流れの方向をキーにする
        # key_trend = 'TRE:{}'.format(self.get_order_type(rates, open_bid).value)

        # キャンドル
        key_candle = self.get_key_candle(rates)

        return ':'.join(x for x in [key_hori_high_low_diff, key_hori_diff, key_candle] if x)

    def get_horizontal_diff_key(self, ma, open_bid, pair):
        """
        現在レートと過去の最高値と安値の乖離
        :param ma: MovingAverageBase
        :param open_bid: float
        :param pair: CurrencyPair
        :return:
        """
        # d25水平で現在レートとの差を取得
        # high_d25 = get_tick_category((ma.high_horizontal_d25 - open_bid) / pair.get_base_tick(), 50)
        # low_d25 = get_tick_category((ma.low_horizontal_d25 - open_bid) / pair.get_base_tick(), 50)

        # d5水平で現在レートとの差を取得
        high_d5 = get_tick_category((ma.high_horizontal_d5 - open_bid) / pair.get_base_tick(), 50)
        low_d5 = get_tick_category((ma.low_horizontal_d5 - open_bid) / pair.get_base_tick(), 50)
        return 'HORI-DIFF:D5:{}:{}'.format(high_d5, low_d5)
