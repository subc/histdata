# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict
import datetime
import time
from module.account.constants import get_units
from module.board.models import AIBoardHistory, AIBoard
from apps.web.views import HTMLAIResult
from module.account.models import Order
from module.oanda.constants import OandaAPIMode
from module.oanda.exceptions import OandaInternalServerError, OandaServiceUnavailableError
from module.oanda.models.api_price import PriceAPI
from utils import CustomBaseCommand


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
                return

        # AIを全部取る
        boards = {ai.id: ai for ai in list(AIBoard.objects.filter())}

        # AIの評価
        self.valuation(price_group, boards)

        # 100取引以上で成績の悪いAIをOFFにする
        self.disable_fool(price_group, boards)

        # 同じAIの排除
        self.disable_same(price_group, boards)

        # 取引数を変更
        self.change_units()

        self.echo("finish")

    def valuation(self, price_group, boards):
        """
        AIの評価
        :param price_group:
        :param boards:
        :return:
        """
        self.echo('AI valuation')
        term = Order.get_close_by_scope(datetime.timedelta(days=0),
                                        datetime.timedelta(days=14))

        ai_group = self.group_by_ai(term, boards)
        default_unit = AIBoard.get_enable_and_main()[0].units
        for ai in ai_group:
            ai.set_current_tick(price_group)
            evaluate(ai, price_group, default_unit)

    def disable_fool(self, price_group, boards):
        """
        100取引以上で成績の悪いAIをOFFにする
        :param price_group:
        :param boards:
        :return:
        """
        self.echo('Fool AI DISABLE')
        term = Order.get_close_by_scope(datetime.timedelta(days=0),
                                        datetime.timedelta(days=365))

        ai_group = self.group_by_ai(term, boards)
        disable_fool_ai(ai_group, price_group)

    def disable_same(self, price_group, boards):
        """
        同じAIの排除
        :param price_group:
        :param boards:
        :return:
        """
        # 14日分の取引の取得
        term = Order.get_close_by_scope(datetime.timedelta(days=0),
                                        datetime.timedelta(days=14))

        ai_group = self.group_by_ai(term, boards)

        self.echo('SAME AI DISABLE')
        disable_same_ai(ai_group, price_group)

    def group_by_ai(self, orders, boards):
        """
        AI毎にオーダーを集計するよ

        :rtype : list of HTMLAIResult
        """
        ai_dict = defaultdict(list)
        for o in orders:
            board = boards[o.ai_board_id]

            # disableAIの排除
            if not board.enable:
                continue
            ai_dict[o.ai_board_id] += [o]
        r = []
        for key in ai_dict:
            r.append(HTMLAIResult(ai_dict[key]))

        r = sorted(r, key=lambda x: x.board.id, reverse=True)
        return r

    def change_units(self):
        """
        取引数の変更
        """
        ai_group = AIBoard.get_enable_and_main()
        ai_count = len(ai_group)
        before_units = ai_group[0].units
        after_units = get_units(10000, ai_count)

        # 差が5以下なら何もしない
        #if abs(after_units - before_units) <= 5:
        #    return

        # 0以下ならエラー
        if after_units <= 0:
            raise ValueError

        # 10000以上ならエラー
        if after_units > 10000:
            raise ValueError

        # update
        for ai in ai_group:
            if ai.elite:
                # エリートは2倍
                ai.units = after_units * 2
            else:
                ai.units = after_units
            ai.save()


def evaluate(ai, price_group, default_unit):
    """
    AI を評価して更新する

    # 200のとき
    平均取引回数8回以上、かつ、合計-150tick以下のとき取引量1となる

    # 1のとき
    平均取引回数8回以上、かつ、合計+100tick以上のとき取引量200となる

    :param ai: HTMLAIResult
    :param price_group: dict of PriceAPIModel
    :param default_unit: int
    """
    # 取引回数が10未満だ
    count = len(Order.get_close_order_by_board(ai.board))
    if count < 10:
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
            rank_up_down(ai.board, default_unit, price, 0)
    else:
        # 高評価AIのとき
        if ai.sum_tick <= -150 or total_tick <= -150:
            rank_up_down(ai.board, 1, price, 0)
        if ai.sum_tick >= 1000 and total_tick >= 1000:
            rank_up_down(ai.board, default_unit, price, 1)


def rank_up_down(board, after_units, price, elite):
    """
    取引量のランク変動
    :param board:AIBoard
    :param after_units:int
    :param price:PriceAPIModel
    :param elite:int
    """
    before_units = board.units

    # 記録
    history = AIBoardHistory.create(board, after_units, price)

    # AIBoardの更新
    board.update_units(history, elite)

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
        # 取引数が100未満のAIは対象外
        if ai.count < 100:
            continue
        disable_ids += _same_ai(ai, ai_group, price_group)


def disable_fool_ai(ai_group, price_group):
    """
    無能なAIをOFFにする
    :param ai_group: list if HTMLAIResult
    :param price_group: dict of PriceAPIModel
    """
    for ai in ai_group:
        # 取引数が50未満のAIは対象外
        if ai.count < 50:
            continue

        # 利益が-1000以上なら対象外
        if ai.sum_tick > -1000:
            continue

        # 無効にする
        message = "FOOL AI{}!!".format(ai.board.id)
        print message
        ai.set_current_tick(price_group)
        ai.board.trade_stop(message, ai.count, ai.sum_tick, ai.open_position_tick)  # 停止


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
            message = "SAME AI!! BASE:{} DISABLE_TARGET:{}".format(ai.board.id, _ai.board.id)
            _ai.board.trade_stop(message, ai.count, ai.sum_tick, ai.open_position_tick)  # 停止
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
