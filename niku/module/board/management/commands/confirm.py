# -*- coding: utf-8 -*-
"""
注文の状況を確かめる
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
from module.board.models import AIBoard, Order
from module.genetic.models.parameter import OrderType
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_orders import OrdersAPI
from module.oanda.models.api_price import PriceAPI
from module.rate import CurrencyPairToTable, Granularity
from module.oanda.models.api_transactions import TransactionsAPI


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        print 'confirm'

        # transactions APIにアクセス
        account_group = AIBoard.get_accounts()

        for account in account_group:
            self.access(account)

    def access(self, account):
        print TransactionsAPI(OandaAPIMode.PRODUCTION, account).get_all()


        # historyにTransactionを全て記録


        # イベント毎に更新を行う

        # MARKET_ORDER_CREATE
        # 整合性チェック

        # STOP_LOSS_FILLED
        # TAKE_PROFIT_FILLED
        # 利益として記録

