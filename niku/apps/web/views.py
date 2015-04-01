# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict
import datetime
from django.utils.functional import cached_property
from ..base.views import BaseView
from module.account.models import Order
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_account import AccountAPI
from module.oanda.models.api_positions import PositionsAPI
from module.oanda.models.api_price import PriceAPI
from module.rate import CurrencyPair


class IndexView(BaseView):
    """
    アカウント情報のサマリーページ
    """
    template_name = "web/index.html"

    def get(self, request, *args, **kwargs):
        # account
        account = AccountAPI(OandaAPIMode.PRODUCTION, 6181277).get_all()

        # positions
        positions = PositionsAPI(OandaAPIMode.PRODUCTION, 6181277).get_all()
        is_valid, html_orders = self.get_orders(positions)

        # order
        c_order_all = HTMLCloseOrder('ALL', Order.get_close())
        close_orders = [c_order_all]
        for index in range(11):
            o = HTMLCloseOrder('{}DAY'.format(index), Order.get_close_by_scope(datetime.timedelta(days=index),
                                                                               datetime.timedelta(days=index + 1)))
            close_orders.append(o)

        # order 1week
        order_week = Order.get_close_by_scope(datetime.timedelta(days=0),
                                              datetime.timedelta(days=7))
        ai_result = self.ai_aggregation(order_week)

        return self.render_to_response({
            'account': account,
            'is_valid': is_valid,
            'html_orders': html_orders,
            'close_orders': close_orders,
            'ai_result': ai_result,
        })

    def get_orders(self, positions):
        # OPENなポジション取得
        orders = Order.get_open()
        orders_dict = {}
        for pair in CurrencyPair:
            orders_dict[pair] = 0
            for order in orders:
                if order.currency_pair == pair:
                    orders_dict[pair] += order.units if order.buy else order.units * -1

        # 現在の価格を調査
        print '~~~~~~~~~~~~~~~~~'
        print 'Current Position Profit'
        print '~~~~~~~~~~~~~~~~~'
        html_orders = []
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
            h = HTMLOrder(pair, position, price_group)
            html_orders.append(h)
        return orders_dict, html_orders

    def ai_aggregation(self, orders):
        """
        AI毎にオーダーを集計するよ
        """
        ai_dict = defaultdict(list)
        for o in orders:
            ai_dict[o.ai_board_id] += [o]
        r = []
        for key in ai_dict:
            r.append(HTMLAIResult(ai_dict[key]))

        r = sorted(r, key=lambda x: x.sum_tick, reverse=True)
        return r


class HTMLOrder(object):
    def __init__(self, pair, position, price_group):
        self.pair = pair
        self.position = position
        self.price = price_group[pair]

    @property
    def yen(self):
        return self.pair.units_to_yen(self.tick, self.position.units)

    @property
    def tick(self):
        position = self.position
        price = self.price
        if position.is_buy:
            print 'BUY MARKET:{} POSITION:{}'.format(price.bid, position.avgPrice)
            tick = (price.bid - position.avgPrice) / self.pair.get_base_tick()
        elif position.is_sell:
            print 'SELL MARKET:{} POSITION:{}'.format(price.ask, position.avgPrice)
            tick = (position.avgPrice - price.ask) / self.pair.get_base_tick()
        return tick

    @property
    def side(self):
        if self.position.is_buy:
            return 'BUY'
        elif self.position.is_sell:
            return 'SELL'
        return 'None'

    @property
    def side_bool(self):
        return bool(self.yen > 0)


class HTMLCloseOrder(object):
    def __init__(self, tag, orders):
        self.tag = tag
        self.orders = orders

    @cached_property
    def profit(self):
        return sum([o.profit for o in self.orders])

    @cached_property
    def profit_tick(self):
        return sum([o.profit_tick for o in self.orders])

    @cached_property
    def count(self):
        return len(self.orders)

    @cached_property
    def avg_tick(self):
        if self.count == 0:
            return 0
        return float(self.profit_tick / self.count)


class HTMLAIResult(object):
    def __init__(self, orders):
        if not orders:
            raise ValueError

        self.orders = orders

    @cached_property
    def board(self):
        return self.orders[0].board

    @property
    def pair(self):
        return self.orders[0].currency_pair
                #
                # <th>unit</th>
                # <th>sum tick</th>
                # <th>avg tick</th>
                # <th>count</th>

    @cached_property
    def units(self):
        return self.board.units

    @cached_property
    def sum_tick(self):
        return sum([o.profit_tick for o in self.orders])

    @cached_property
    def count(self):
        return len(self.orders)

    @cached_property
    def avg_tick(self):
        return float(self.sum_tick / self.count)