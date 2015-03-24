# -*- coding: utf-8 -*-
"""
boardを更新する
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import requests
from ...constans import TEST_HEADER, TEST_HOST
from django.core.management import BaseCommand
from module.board.models import AIBoard
from module.genetic.models.parameter import OrderType
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_orders import OrdersAPI
from module.oanda.models.api_price import PriceAPI
from module.rate import CurrencyPairToTable, Granularity


class Command(BaseCommand):
    CACHE_PREV_RATES = {}

    def handle(self, *args, **options):
        self.run()

    def run(self):
        # price取る
        price_group = PriceAPI(OandaAPIMode.PRODUCTION).get_all()

        # AIインスタンス生成
        ai_board_group = AIBoard.get_all()
        for ai_board in ai_board_group:
            self.check(ai_board, price_group)

    def check(self, ai_board, price_group):
        for x in xrange(10):
            order1 = self.order(ai_board, price_group)
            order2 = self.order(ai_board, price_group)
            self.test(order1, order2)

    def order(self, ai_board, price_group):
        ai = ai_board.get_ai_instance()
        price = price_group.get(ai.currency_pair, None)
        prev_rates = self.get_prev_rates(ai.currency_pair, Granularity.H1)
        order_ai = ai.get_order_ai(prev_rates, price.bid, price.time)
        assert order_ai is not None
        assert type(order_ai.order_type) == OrderType
        return order_ai

    def test(self, order1, order2):
        if order1 is None and order2 is None:
            return True
        if order1 is None:
            raise ValueError
        if order2 is None:
            raise ValueError
        if type(order1) != type(order2):
            raise ValueError
        assert order1.order_type == order2.order_type, '{}:{}'.format(order1.order_type, order2.order_type)
        assert order1.limit == order2.limit
        assert order1.stop_limit == order2.stop_limit

    def get_prev_rates(self, currency_pair, granularity):
        key = self._get_key(currency_pair, granularity)
        r = self.CACHE_PREV_RATES.get(key)
        if r:
            return r
        prev_rates = CurrencyPairToTable.get_table(currency_pair, granularity).get_new_record_by_count(10000)
        self.CACHE_PREV_RATES[key] = prev_rates
        return prev_rates

    def _get_key(self, currency_pair, granularity):
        return 'RATE:{}:{}'.format(currency_pair.value, granularity.value)