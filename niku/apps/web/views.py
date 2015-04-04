# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict
import datetime
from django.utils.functional import cached_property
from ..base.views import BaseView
from module.account.models import Order
from module.board.models import AIBoard
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_account import AccountAPI
from module.oanda.models.api_positions import PositionsAPI
from module.oanda.models.api_price import PriceAPI
from module.rate import CurrencyPair
from module.account.models.kill_switch import KillSwitch
from module.account.constants import *


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
        price_group = PriceAPI(OandaAPIMode.PRODUCTION).get_all()
        is_valid, html_orders = self.get_orders(positions, price_group)

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
        for ai in ai_result:
            ai.set_current_tick(price_group)

        # open orders
        open_orders = Order.get_open()
        self.set_profit(open_orders, price_group)
        open_orders = sorted(open_orders, key=lambda x: (x._currency_pair, x.current_profit_tick))

        # 統計情報
        ai_total_units = sum(ai.units for ai in ai_result if ai.board.enable)
        total_position_units = sum([o.position.units for o in html_orders])
        _percent = float(float(total_position_units * 100) / float(ai_total_units * 10))
        position_percent = '%.2f' % _percent
        open_position_units = sum([o.units for o in open_orders])
        _percent = float(float(open_position_units * 100) / float(ai_total_units * 10))
        open_position_percent = '%.2f' % _percent
        # 資金拘束
        _percent = float(float(account.get('marginUsed')) / float(account.get('balance'))) * 100
        account_margin_percent = '%.2f' % _percent
        # リスク系の統計情報
        ai_count = AIBoard.objects.filter(units__gt=1,
                                          enable=1).count()
        foresee_daily_risk = int(ai_count * UNITS * DAILY_RISK_COEFFICIENT)
        foresee_margin = int(ai_count * UNITS * MARGIN_COEFFICIENT)
        daily_risk = int(sum([o.profit for o in order_week]) / 5)

        return self.render_to_response({
            'account': account,
            'is_valid': is_valid,
            'kill_sw': KillSwitch.is_active(),
            'html_orders': html_orders,
            'open_orders': open_orders,
            'close_orders': close_orders,
            'ai_result': ai_result,
            # 統計情報
            'ai_total_units': ai_total_units,
            'total_position_units': total_position_units,
            'open_position_units': open_position_units,
            'position_percent': position_percent,
            'open_position_percent': open_position_percent,
            'account_margin_percent': account_margin_percent,
            'ai_count': ai_count,
            'foresee_daily_risk': foresee_daily_risk,
            'foresee_margin': foresee_margin,
            'daily_risk': daily_risk,
        })

    def get_orders(self, positions, price_group):
        # OPENなポジション取得
        orders = Order.get_open()
        orders_dict = {}
        for pair in CurrencyPair:
            orders_dict[pair] = 0
            for order in orders:
                if order.currency_pair == pair:
                    orders_dict[pair] += order.units if order.buy else order.units * -1

        # valid
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

        # 現在の価格を調査
        print '~~~~~~~~~~~~~~~~~'
        print 'Current Position Profit'
        print '~~~~~~~~~~~~~~~~~'
        html_orders = []
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
        return is_valid, html_orders

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

    def set_profit(self, open_orders, price_group):
        for o in open_orders:
            price = price_group.get(o.currency_pair)
            _price = price.bid if o.buy else price.ask
            if o.buy:
                tick = (_price - o.real_open_rate) / o.currency_pair.get_base_tick()
            else:
                tick = (o.real_open_rate - _price) / o.currency_pair.get_base_tick()
            o.current_profit_tick = tick


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

    @cached_property
    def pair(self):
        return self.orders[0].currency_pair

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

    def set_current_tick(self, price_group):
        """
        未決済ポジションのtickを設定する
        :param price_group: dict of PriceAPIModel
        """
        price = price_group.get(self.pair)
        open_orders = Order.get_open_order_by_board(self.board)
        self.open_position_tick = sum([o.get_current_profit_tick(price) for o in open_orders])
        self.open_position_count = len(open_orders)