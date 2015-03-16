# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
from module.board.models import AIBoard, Order
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_price import PriceAPI


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        print 'order'
        # price取る
        price_group = PriceAPI(OandaAPIMode.PRODUCTION).get_all()

        # AIインスタンス生成
        ai_board_group = AIBoard.get_enable()
        for ai_board in ai_board_group:
            self.order(ai_board, price_group)

    def order(self, ai_board, price_group):
        """
        発注したらTrueを返却
        :param ai_board: AIBoard
        :param price_group: dict of PriceAPIModel
        :rtype : bool
        """
        ai = ai_board.get_ai_instance()
        price = price_group.get(ai.currency_pair, None)

        # 価格は正常？
        if price is None or not price.is_active():
            return False

        # ポジション数による購入制限と時間による購入制限
        if ai_board.can_order():
            return False

        # レートが正常ではない
        prev_rates = hoge
        if not prev_rates:
            return False

        # 購入判断
        order_ai = ai.get_order_ai(prev_rates, price.bid, price.c_time)

        if order_ai is None:
            return False

        # 仮注文発砲
        Order.pre_order(order_ai)

        # API注文

        # 注文成立したあと
