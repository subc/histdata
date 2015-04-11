# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.core.management import BaseCommand
import time
import sys
import pytz
from module.account.models import Order
from module.board.models import AIBoard
from module.genetic.models.parameter import OrderType
from module.oanda.constants import OandaAPIMode
from module.oanda.exceptions import OandaServiceUnavailableError, OandaInternalServerError
from module.oanda.models.api_account import AccountAPI
from module.oanda.models.api_orders import OrdersAPI
from module.oanda.models.api_price import PriceAPI
from module.rate import CurrencyPairToTable, Granularity, CurrencyPair
from utils import CustomBaseCommand


class Command(CustomBaseCommand):
    """
    BoardAIを利用して発注する
    """
    CACHE_PREV_RATES = {}

    def handle(self, *args, **options):
        print '********************************'
        self.echo('open start')
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
        except Exception as e:
            self.critical_error('open', e)

        # 3秒停止
        time.sleep(3)

    def run(self):
        # 証拠金チェック
        account = AccountAPI(OandaAPIMode.PRODUCTION, 6181277).get_all()
        if int(account.get('marginAvail')) < 10000:
            self.echo('MARGIN EMPTY!! marginAvail:{}'.format(int(account.get('marginAvail'))))
            time.sleep(3000)

        # price取る
        price_group = PriceAPI(OandaAPIMode.PRODUCTION).get_all()

        # AIインスタンス生成
        order_group = []
        ai_board_group = AIBoard.get_all()

        # 仮発注
        now = datetime.datetime.now(tz=pytz.utc)
        for ai_board in ai_board_group:
            order = self.pre_order(ai_board, price_group, now)
            if order:
                order_group.append(order)

        # 発注
        self.order(order_group, price_group)

    def pre_order(self, ai_board, price_group, now):
        """
        発注したらTrueを返却
        :param ai_board: AIBoard
        :param price_group: dict of PriceAPIModel
        :param now: datetime
        :rtype : bool
        """
        ai = ai_board.get_ai_instance()
        price = price_group.get(ai.currency_pair, None)

        # 価格は正常？
        if price is None:
            return None
        if not price.is_active():
            # print 'price not active'
            return None

        # レートが正常ではない
        prev_rates = self.get_prev_rates(ai.currency_pair, Granularity.H1)
        if not prev_rates:
            return None
        prev_rate = prev_rates[-1]

        # 前回レートから乖離が3分以内
        if now - prev_rate.start_at > datetime.timedelta(seconds=60 * 3):
            # print 'ORDER TIME IS OVER'
            return None

        # ポジション数による購入制限と時間による購入制限
        if not ai_board.can_order(prev_rate):
            # print 'TIME OR POSITION LIMIT'
            return None

        # 購入判断 AIのシミュレーションと同じ様に、midのみを対象にして売買を決定する
        order_ai = ai.get_order_ai(prev_rates, price.mid, price.time, is_production=True)

        if order_ai is None:
            return None
        if order_ai.order_type == OrderType.WAIT:
            return None

        # 仮注文発砲
        order = Order.pre_open(ai_board, order_ai, price, prev_rate.start_at)
        return order

    def order(self, order_group, price_group):
        """
        プレオーダーをサマリーとって実際に発注する
        :param order_group: list of Order
        :param price_group: dict of PriceAPIModel
        :return:
        """
        # サマリー取る
        order_dict = {x: 0 for x in CurrencyPair}
        for order in order_group:
            if order.buy:
                order_dict[order.currency_pair] += order.units
            else:
                order_dict[order.currency_pair] -= order.units
        print order_dict

        # 発注
        api_response_dict = {}
        for key in order_dict:
            if order_dict[key] == 0:
                print '{}:NO ORDER'.format(key)
                continue
            print '{}:ORDER!'.format(key)
            units = order_dict[key]
            api_response_dict[key] = OrdersAPI(OandaAPIMode.PRODUCTION, 6181277).post(key, units, tag='open')

        # DB更新
        for order in order_group:
            order.open(price_group.get(order.currency_pair))

    def get_prev_rates(self, currency_pair, granularity):
        key = self._get_key(currency_pair, granularity)
        print key
        r = self.CACHE_PREV_RATES.get(key)
        if r:
            return r
        prev_rates = CurrencyPairToTable.get_table(currency_pair, granularity).get_new_record_by_count(10000)
        self.CACHE_PREV_RATES[key] = prev_rates
        return prev_rates

    def _get_key(self, currency_pair, granularity):
        return 'RATE:{}:{}'.format(currency_pair.value, granularity.value)