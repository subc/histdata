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
from module.board.models import AIBoard, Order
from module.genetic.models.parameter import OrderType
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_orders import OrdersAPI
from module.oanda.models.api_price import PriceAPI
from module.rate import CurrencyPairToTable, Granularity


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        # price取る
        price_group = PriceAPI(OandaAPIMode.PRODUCTION).get_all()

        # AIインスタンス生成
        ai_board_group = AIBoard.get_all()
        for ai_board in ai_board_group:
            self.order(ai_board, price_group)

    def order(self, ai_board, price_group):
        ai = ai_board.get_ai_instance()
        price = price_group.get(ai.currency_pair, None)
        prev_rates = CurrencyPairToTable.get_table(ai.currency_pair, Granularity.H1).get_new_record_by_count(10000)
        order_ai = ai.get_order_ai(prev_rates, price.bid, price.time)
        assert order_ai is not None
        assert type(order_ai.order_type) == OrderType
