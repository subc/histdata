# -*- coding: utf-8 -*-
"""
注文の状況を確かめる
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.core.management import BaseCommand
import time
import pytz
from module.board.models import AIBoard
from module.oanda.constants import OandaAPIMode
from module.oanda.exceptions import OandaInternalServerError, OandaServiceUnavailableError
from module.oanda.models.api_transactions import TransactionsAPI
from module.account.models import OandaTransaction
from utils import CustomBaseCommand


class Command(CustomBaseCommand):
    def handle(self, *args, **options):
        print '********************************'
        self.echo('confirm start')
        self.check_kill_switch()
        try:
            self.run()
        except OandaServiceUnavailableError:
            # 土日メンテ中のとき
            self.echo("ServiceUnavailableError")
            time.sleep(60)
        except OandaInternalServerError:
            # 土日メンテ中のとき
            self.echo("OandaInternalServerError")
            time.sleep(60)

    def run(self):
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