# -*- coding: utf-8 -*-
"""
注文の状況を確かめる
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import time
from module.board.models import AIBoard
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_transactions import TransactionsAPI
from module.account.models import OandaTransaction


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