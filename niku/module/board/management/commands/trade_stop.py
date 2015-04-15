# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import time
from module.account.models import OandaTransaction, KillSwitch
from module.oanda.constants import OandaAPIMode
from module.oanda.exceptions import OandaServiceUnavailableError, OandaInternalServerError
from module.oanda.models.api_account import AccountAPI
from utils import CustomBaseCommand


class Command(CustomBaseCommand):
    """
    AIのデータ不整合が発生して注文が連続して発生していたら
    手数料で死ぬので取引強制終了する
    """
    ORDER_LIMIT = 150  # 1時間でこの数以上のオーダー飛ばしてたら危険
    BALANCE = 28 * 10000  # アカウントがこの額以下になったら停止

    def handle(self, *args, **options):
        print '********************************'
        self.echo('trade stop start')
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

        self.echo('trade stop finish')
        time.sleep(30)

    def run(self):
        # 特定金額以下にアカウント残高が減少
        self.check_account_balance()

        # 1時間以内に注文しすぎ
        self.check_order_count()

    def check_account_balance(self):
        # 特定金額以下にアカウント残高が減少
        account = AccountAPI(OandaAPIMode.PRODUCTION, 6181277).get_all()
        balance = float(account.get('balance'))
        unrealizedPl = float(account.get('unrealizedPl'))
        self.echo('balance:{} unrealizedPl:{}'.format(balance, unrealizedPl))

        # 口座残高
        if balance > self.BALANCE:
            return
        if balance + unrealizedPl > self.BALANCE:
            return

        # キルスイッチ有効
        self.echo('KILL SWITCH ON! balance:{} unrealizedPl:{}'.format(balance, unrealizedPl))
        KillSwitch.create('TRADE STOP:CHECK-ACCOUNT-BALANCE',
                          'balance:{} unrealizedPl:{}'.format(balance, unrealizedPl))

    def check_order_count(self):
        # 1時間以内に注文しすぎ
        count = OandaTransaction.get_market_order_count()

        # カウントが水準以下なら何もしない
        if count < self.ORDER_LIMIT:
            return

        # キルスイッチON
        self.echo('KILL SWITCH ON! check_order_count is {}'.format(count))
        KillSwitch.create('TRADE STOP:CHECK-ORDER-COUNT', 'COUNT IS :{}'.format(count))