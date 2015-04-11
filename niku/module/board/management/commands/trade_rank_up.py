# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict
import datetime
import time
from module.board.models import AIBoardHistory
from apps.web.views import HTMLAIResult
from module.account.models import Order
from module.oanda.constants import OandaAPIMode
from module.oanda.exceptions import OandaInternalServerError, OandaServiceUnavailableError
from module.oanda.models.api_price import PriceAPI
from utils import CustomBaseCommand


UNITS = 200


class Command(CustomBaseCommand):
    """
    取引量を変化させる

    # scope
    1週間の取引を参照する。

    # ステータスは二つ
    取引量200と取引量1

    # 200のとき
    平均取引回数8回以上、かつ、合計-150tick以下のとき取引量1となる

    # 1のとき
    平均取引回数8回以上、かつ、合計+100tick以上のとき取引量200となる
    """

    def handle(self, *args, **options):
        print '********************************'
        self.echo('trade rank up start')
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

        time.sleep(120)

    def run(self):
        # 現在価格の取得
        price_group = PriceAPI(OandaAPIMode.PRODUCTION).get_all()

        # メンテ中なら何もしない
        for key in price_group:
            price = price_group[key]
            if price.is_maintenance:
                self.echo('MAINTENANCE NOW!!')

        # 1週間分の取引の取得
        order_week = Order.get_close_by_scope(datetime.timedelta(days=0),
                                              datetime.timedelta(days=7))

        ai_group = self.group_by_ai(order_week)

        for ai in ai_group:
            ai.set_current_tick(price_group)
            evaluate(ai, price_group)

        # 同じAIの排除
        self.echo('SAME AI DISABLE')
        disable_same_ai(ai_group, price_group)

    def group_by_ai(self, orders):
        """
        AI毎にオーダーを集計するよ

        :rtype : list of HTMLAIResult
        """
        ai_dict = defaultdict(list)
        for o in orders:
            ai_dict[o.ai_board_id] += [o]
        r = []
        for key in ai_dict:
            r.append(HTMLAIResult(ai_dict[key]))

        r = sorted(r, key=lambda x: x.board.id, reverse=True)
        return r


def evaluate(ai, price_group):
    """
    AI を評価して更新する

    # 200のとき
    平均取引回数8回以上、かつ、合計-150tick以下のとき取引量1となる

    # 1のとき
    平均取引回数8回以上、かつ、合計+100tick以上のとき取引量200となる

    :param ai: HTMLAIResult
    :param price_group: dict of PriceAPIModel
    """
    # 取引回数が8未満だ
    count = len(Order.get_close_order_by_board(ai.board))
    if count < 8:
        return

    price = price_group.get(ai.pair)
    # 未決済ポジションの利益計算
    open_orders = Order.get_open_order_by_board(ai.board)
    open_position_tick = sum([o.get_current_profit_tick(price) for o in open_orders])
    total_tick = ai.sum_tick + open_position_tick
    print "AI:{} VER:{} CLOSE:{} OPEN:{} TOTAL:{}".format(ai.board.id,
                                                          ai.board.version,
                                                          ai.sum_tick,
                                                          open_position_tick,
                                                          total_tick)

    if ai.units == 1:
        # 低評価AIのとき
        if ai.sum_tick >= 100 and total_tick >= 100:
            board = ai.board
            rank_up_down(board, UNITS, price)
    else:
        # 高評価AIのとき
        if ai.sum_tick <= -150 or total_tick <= -150:
            board = ai.board
            rank_up_down(board, 1, price)


def rank_up_down(board, after_units, price):
    """
    取引量のランク変動
    :param board:AIBoard
    :param after_units:int
    :param price:PriceAPIModel
    """
    before_units = board.units

    # 記録
    history = AIBoardHistory.create(board, after_units, price)

    # AIBoardの更新
    board.update_units(history)

    # print
    print "AI:{} BEFORE:{} AFTER:{}".format(board.id,
                                            before_units,
                                            board.units)


def disable_same_ai(ai_group, price_group):
    """
    同じAIをOFFにする
    :param ai_group: list if HTMLAIResult
    :param price_group: dict of PriceAPIModel
    """
    disable_ids = []
    for ai in ai_group:
        # 既にDISABLEのAIは対象外
        if ai.board.id in disable_ids:
            continue
        # 取引数が20未満のAIは対象外
        if ai.count < 20:
            continue
        disable_ids += _same_ai(ai, ai_group, price_group)


def _same_ai(ai, ai_group, price_group):
    """
    同じAIをOFFにして,OFFにしたAIBoardIDを返却
    :param ai_group: list if HTMLAIResult
    :param price_group: dict of PriceAPIModel
    """
    b = ai.board
    disable_ai_group = []
    for _ai in ai_group:
        # 自分自身は無視
        if b.id == _ai.board.id:
            continue
        # 通貨ペア異なっていれば無視
        if ai.pair != _ai.pair:
            continue
        if same(ai, _ai):
            _ai.board.trade_stop()  # 停止
            disable_ai_group.append(_ai)
    return [ai.board.id for ai in disable_ai_group]


def same(ai, ai2):
    """
    2つのAIが同じならTrue
    """
    # クローズした取引tickが異なれば対象外
    if ai.sum_tick != ai2.sum_tick:
        return False
    # オープン中のポジションのtickが異なれば対象外
    if ai.open_position_tick != ai2.open_position_tick:
        return False

    print "SAME AI!! {}:{}".format(ai.board.id, ai2.board.id)
    return True
