# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import time
import sys
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
        print 'order'
        # price取る
        price_group = PriceAPI(OandaAPIMode.PRODUCTION).get_all()

        ct = 0

        # AIインスタンス生成
        ai_board_group = AIBoard.get_enable()
        for ai_board in ai_board_group:
            if ct % 5 == 0:
                # price取る
                price_group = PriceAPI(OandaAPIMode.PRODUCTION).get_all()

            self.order(ai_board, price_group)
            ct += 1

        # 30秒停止
        time.sleep(30)

    def order(self, ai_board, price_group):
        """
        発注したらTrueを返却
        :param ai_board: AIBoard
        :param price_group: dict of PriceAPIModel
        :rtype : bool
        """
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'START AI BOARD:{} UNITS:{}'.format(ai_board.id, ai_board.units)
        ai = ai_board.get_ai_instance()
        price = price_group.get(ai.currency_pair, None)

        # 価格は正常？
        if price is None:
            return False
        if not price.is_active():
            print 'price not active'
            return False

        # レートが正常ではない
        prev_rates = CurrencyPairToTable.get_table(ai.currency_pair, Granularity.H1).get_new_record_by_count(10000)
        if not prev_rates:
            return False
        prev_rate = prev_rates[-1]

        # ポジション数による購入制限と時間による購入制限
        if not ai_board.can_order(prev_rate):
            print '時間かポジション数による購入制限'
            return False

        # 購入判断
        order_ai = ai.get_order_ai(prev_rates, price.bid, price.time)

        if order_ai is None:
            return False
        if order_ai.order_type == OrderType.WAIT:
            return False

        order_ai.print_member()

        # 仮注文発砲
        order = Order.pre_order(ai_board, order_ai, price, prev_rate.start_at)

        # API注文
        api_response = OrdersAPI(ai_board.get_oanda_api_mode(), ai_board.account).post(order)

        # 注文成立情報の記録
        order.set_order(api_response)

        # try:
        #     api_response = OrdersAPI(ai_board.get_oanda_api_mode(), ai_board.account).post(order)
        #
        #     # 注文成立情報の記録
        #     order.set_order(api_response)
        # except Exception as e:
        #     print sys.exc_info()
        #     order.set_order_error(e)
