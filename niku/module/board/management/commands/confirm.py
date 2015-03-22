# -*- coding: utf-8 -*-
"""
注文の状況を確かめる
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import time
from module.board.models import AIBoard, Order
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_transactions import TransactionsAPI
from module.oanda.models.oanda import OandaTransaction


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        print 'confirm'

        # transactions APIにアクセス
        account_group = AIBoard.get_accounts()

        for account in account_group:
            self.access(account)

        # 120秒停止
        time.sleep(120)

    def access(self, account):
        oanda_transactions = TransactionsAPI(OandaAPIMode.PRODUCTION, account).get_all()

        # historyにTransactionを全て記録
        OandaTransaction.bulk_write(account, oanda_transactions)

        # イベント毎に更新を行う
        for transaction in oanda_transactions:
            # 整合性チェック
            Order.confirm(transaction)

            # ポジションクローズの記録
            Order.close(transaction)