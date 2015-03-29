# -*- coding: utf-8 -*-
"""
ポジションとDBの値の整合性を確かめる
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.core.management import BaseCommand
import time
import pytz
from module.board.models import AIBoard
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_account import AccountAPI
from module.oanda.models.api_positions import PositionsAPI
from module.oanda.models.api_price import PriceAPI
from module.oanda.models.api_transactions import TransactionsAPI
from module.account.models import OandaTransaction, Order
from module.rate import CurrencyPair
from utils import CustomBaseCommand


class Command(CustomBaseCommand):
    def handle(self, *args, **options):
        print '********************************'
        self.echo('check_start')
        self.check_kill_switch()
        self.run()

    def run(self):

        # ポジション取得
        positions = PositionsAPI(OandaAPIMode.PRODUCTION, 6181277).get_all()

        # OPENなポジション取得
        orders = Order.get_open()
        orders_dict = {}
        for pair in CurrencyPair:
            orders_dict[pair] = 0
            for order in orders:
                if order.currency_pair == pair:
                    orders_dict[pair] += order.units if order.buy else order.units * -1

        # 比較
        print '~~~~~~~~~~~~~~~~~'
        print 'Current Position Market DB diff'
        print '~~~~~~~~~~~~~~~~~'
        is_valid = False
        for pair in CurrencyPair:
            position = positions.get(pair, None)
            units = orders_dict.get(pair, None)
            if position is None and units == 0:
                print '[{}] IS ALL NONE'.format(pair.name)
            elif position is None:
                print '[{}] API position:None DB units summary:{}'.format(pair.name, units)
                is_valid = True
            else:
                print '[{}] API position:{} DB units summary:{}'.format(pair.name, position.units, units)
                is_valid = not position.equals_units(units)
        print '-----------------'
        # oanda の現在値を取得
        account = AccountAPI(OandaAPIMode.PRODUCTION, 6181277).get_all()
        print 'balance:{}'.format(account.get('balance'))

        # 現在の価格を調査
        print '~~~~~~~~~~~~~~~~~'
        print 'Current Position Profit'
        print '~~~~~~~~~~~~~~~~~'
        price_group = PriceAPI(OandaAPIMode.PRODUCTION).get_all()
        for pair in CurrencyPair:
            price = price_group[pair]
            position = positions.get(pair, None)

            # ポジがないときは何もしない
            if position is None:
                continue

            if position.is_buy:
                print 'BUY MARKET:{} POSITION:{}'.format(price.bid, position.avgPrice)
                tick = (price.bid - position.avgPrice) / pair.get_base_tick()
            elif position.is_sell:
                print 'SELL MARKET:{} POSITION:{}'.format(price.ask, position.avgPrice)
                tick = (position.avgPrice - price.ask) / pair.get_base_tick()
            else:
                raise ValueError
            print '[{}] tick:{} units:{} profit:{}'.format(pair.name,
                                                           tick,
                                                           position.units,
                                                           pair.units_to_yen(tick, position.units))

        # データの状況を確認
        print '~~~~~~~~~~~~~~~~~'
        print 'Current Position Market DB diff'
        print '~~~~~~~~~~~~~~~~~'
        print 'IS_VALID : {}'.format(is_valid)
