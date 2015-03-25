# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.db import models
import pytz
from module.account.models import Order


class AIBoardHistory(models.Model):
    """
    成績
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trade_start_at = models.DateTimeField(default=None, null=True)
    trade_end_at = models.DateTimeField(default=None, null=True)
    trade_stop_at = models.DateTimeField(default=None, null=True)
    ai_board_id = models.PositiveIntegerField(db_index=True)
    version = models.PositiveIntegerField(default=1, null=True, help_text='AIの取引世代')
    trade_count = models.PositiveIntegerField(default=None, null=True)
    before_units = models.PositiveIntegerField()
    after_units = models.PositiveIntegerField()
    is_rank_up = models.PositiveIntegerField(help_text='昇進ならTrue', default=None, null=True)
    profit_summary = models.FloatField()
    profit_average = models.FloatField()
    profit_tick_summary = models.FloatField()
    profit_tick_average = models.FloatField()

    class Meta(object):
        app_label = 'board'

    @classmethod
    def create_if_achieve(cls, board):
        """
        条件を満たしていればcreate
        :param board: AIBoard
        :rtype : AIBoardHistory
        """
        orders = Order.get_by_board(board)
        trade_count = len(orders)
        if trade_count == 0:
            return None
        profit_summary = sum([x.profit for x in orders])
        profit_average = float(profit_summary / trade_count)
        profit_tick_summary = sum([x.profit_tick for x in orders])
        profit_tick_average = float(profit_tick_summary / profit_average)
        can_create, is_rank_up = cls.can_create(board, trade_count, profit_tick_average, profit_tick_summary)
        if not can_create:
            return None
        after_units = cls.get_next_units(board.units, is_rank_up)
        trade_start_at = min([x.created_at for x in orders])
        trade_end_at = max([x.end_at for x in orders])
        return cls.objects.create(trade_start_at=trade_start_at,
                                  trade_end_at=trade_end_at,
                                  ai_board_id=board.id,
                                  version=board.version,
                                  trade_count=trade_count,
                                  before_units=board.version,
                                  after_units=after_units,
                                  is_rank_up=is_rank_up,
                                  profit_summary=profit_summary,
                                  profit_average=profit_average,
                                  profit_tick_summary=profit_tick_summary,
                                  profit_tick_average=profit_tick_average)

    @classmethod
    def can_create(cls, board, trade_count, profit_tick_average, profit_tick_summary):
        """
        生成
        :param board: AIBoard
        :param trade_count: int
        :param profit_tick_average: float
        :param profit_tick_summary: float
        :return: can_create, is_rank_up
        :rtype : bool, bool
        """
        # 5回以上取引していて合計-36以下
        if trade_count >= 5 and profit_tick_summary <= 36:
            return True, False

        # 11回以上取引、平均10以上
        if trade_count >= 11 and profit_tick_average >= 10:
            return True, True

        # 22回以上取引、平均4以上
        if trade_count >= 22 and profit_tick_average >= 4:
            return True, True

        # 22回以上取引、平均0以下
        if trade_count >= 22 and profit_tick_average <= 0:
            return True, False

        return False, None

    @classmethod
    def get_next_units(cls, units, is_rank_up):
        """
        次のunits数を返却

        10
        100
        1000
        5000
        10000
        15000
        20000
        25000
        :param units: int
        :param is_rank_up: bool
        :rtype : int
        """
        # 10000以上のとき
        if units >= 10000:
            if is_rank_up:
                return units + 5000
            else:
                return 5000

        # 5000
        if 10000 > units >= 5000:
            if is_rank_up:
                return 10000
            else:
                return 1000

        # 4999以下11以上
        if 4999 >= units > 0:
            if is_rank_up:
                return min([5000, units * 10])
            else:
                return max([10, units / 10])

    def get_new_history(self, count):
        """
        最新ヒストリーを取得
        :param count: int
        :rtype : list of AIBoardHistory
        """
        return list(AIBoardHistory.objects.filter(ai_board_id=self.ai_board_id).order_by('-version')[:count])

    def can_trade_stop(self):
        """
        取引停止可能かチェックする。停止するときはTrue
        :rtype : bool
        """
        # unitsが11以上のときは、調査しない
        if self.before_units == self.after_units == 10:
            return False

        # 過去10イテレーション以下の時は調査しない
        if self.version <= 10:
            return False

        # 直近10取引をみて、units10が5以上のときは停止
        history_group = self.get_new_history(10)
        count = len([x.units for x in history_group if x.units <= 10])
        if count >= 5:
            return True
        return False

    def trade_stop(self):
        """
        取引停止を記録
        """
        self.trade_end_at = datetime.datetime.now(tz=pytz.utc)
        self.save()