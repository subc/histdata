# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
from module.account.models import Order
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_orders import OrdersAPI
from module.oanda.models.api_price import PriceAPI
from module.rate import CurrencyPair


class Command(BaseCommand):
    """
    account historyを利用してクローズする
    """
    CACHE_PREV_RATES = {}

    def handle(self, *args, **options):
        self.run()

    def run(self):
        print 'close'

        orders = Order.get_open()
        print orders

        # price取る
        price_group = PriceAPI(OandaAPIMode.PRODUCTION).get_all()

        # サマリー取る
        order_dict = {x: 0 for x in CurrencyPair}
        for order in orders:
            if order.can_close(price_group[order.currency_pair]):
                if order.buy:
                    print order.currency_pair, order.units
                    order_dict[order.currency_pair] += order.units
                    print order_dict[order.currency_pair]
                else:
                    print order.currency_pair, order.units
                    order_dict[order.currency_pair] -= order.units
                    print order_dict[order.currency_pair]
        print order_dict

        # 発注
        api_response_dict = {}
        for key in order_dict:
            if order_dict[key] == 0:
                print '{}:発注なし'.format(key)
                continue
            print '{}:発注'.format(key)
            units = order_dict[key]
            api_response_dict[key] = OrdersAPI(OandaAPIMode.PRODUCTION, 6181277).post(key, units)

        # 記録
        for order in orders:
            if order.can_close(price_group[order.currency_pair]):
                order.close(price_group.get(order.currency_pair))
