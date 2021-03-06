# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.core.management import BaseCommand
import time
import pytz
from requests import ConnectionError
from module.account.models import Order
from module.oanda.constants import OandaAPIMode
from module.oanda.exceptions import OandaServiceUnavailableError, OandaInternalServerError
from module.oanda.models.api_orders import OrdersAPI
from module.oanda.models.api_price import PriceAPI
from module.rate import CurrencyPair
from utils import CustomBaseCommand


class Command(CustomBaseCommand):
    """
    account historyを利用してクローズする
    """
    CACHE_PREV_RATES = {}

    def handle(self, *args, **options):
        print '********************************'
        self.echo('close start')
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
        except ConnectionError:
            time.sleep(60)
        except Exception as e:
            self.critical_error('close', e)
        time.sleep(3)

    def run(self):
        orders = Order.get_open()

        # price取る
        price_group = PriceAPI(OandaAPIMode.PRODUCTION).get_all()

        # サマリー取る
        order_dict = {x: 0 for x in CurrencyPair}
        for order in orders:
            if order.can_close(price_group[order.currency_pair]):
                if order.buy:
                    # 反転売買する
                    print order.currency_pair, order.units
                    order_dict[order.currency_pair] -= order.units
                    print order_dict[order.currency_pair]
                else:
                    # 反転売買する
                    print order.currency_pair, order.units
                    order_dict[order.currency_pair] += order.units
                    print order_dict[order.currency_pair]
        print order_dict

        # 発注
        api_response_dict = {}
        for key in order_dict:
            if order_dict[key] == 0:
                print '{}:NO ORDER'.format(key)
                continue
            print '{}:ORDER'.format(key)
            units = order_dict[key]
            api_response_dict[key] = OrdersAPI(OandaAPIMode.PRODUCTION, 6181277).post(key, units, tag='close')

        # 記録
        for order in orders:
            if order.can_close(price_group[order.currency_pair]):
                order.close(price_group.get(order.currency_pair))