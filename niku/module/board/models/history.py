# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.db import models
import pytz
from module.account.models import Order
from .ai import AIBoard


class AIBoardHistory(models.Model):
    """
    成績
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trade_start_at = models.DateTimeField(default=None, null=True)
    trade_end_at = models.DateTimeField(default=None, null=True)
    ai_board_id = models.PositiveIntegerField(db_index=True)
    version = models.PositiveIntegerField(default=1, null=True, help_text='AIの取引世代')
    trade_count = models.PositiveIntegerField(default=None, null=True)
    open_position_count = models.PositiveIntegerField(default=None, null=True)
    open_position_profit = models.FloatField(default=None, null=True)
    open_position_tick = models.FloatField(default=None, null=True)
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
    def create(cls, board, after_units, price):
        """
        注文状況を集計して記録する
        :param board: AIBoard
        :param after_units: int
        :param price: OrderApiModels
        :rtype : AIBoardHistory
        """
        # 未決済のポジションを集計
        open_orders = Order.get_open_order_by_board(board)
        open_position_count = len(open_orders)
        open_position_profit = sum([o.get_current_profit(price) for o in open_orders])
        open_position_tick = sum([o.get_current_profit_tick(price) for o in open_orders])

        # 決済済みのポジションを集計
        orders = Order.get_close_order_by_board(board)
        trade_count = len(orders)
        profit_summary = sum([x.profit for x in orders])
        profit_average = float(profit_summary / trade_count) if trade_count > 0 else 0
        profit_tick_summary = sum([x.profit_tick for x in orders])
        profit_tick_average = float(profit_tick_summary / trade_count) if trade_count > 0 else 0
        is_rank_up = after_units > board.units
        trade_start_at = min([x.created_at for x in orders])
        trade_end_at = max([x.end_at for x in orders])
        return cls.objects.create(trade_start_at=trade_start_at,
                                  trade_end_at=trade_end_at,
                                  ai_board_id=board.id,
                                  version=board.version,
                                  trade_count=trade_count,
                                  before_units=board.units,
                                  after_units=after_units,
                                  is_rank_up=is_rank_up,
                                  profit_summary=profit_summary,
                                  profit_average=profit_average,
                                  profit_tick_summary=profit_tick_summary,
                                  profit_tick_average=profit_tick_average,
                                  open_position_count=open_position_count,
                                  open_position_profit=open_position_profit,
                                  open_position_tick=open_position_tick)

    @property
    def board(self):
        return AIBoard.get(self.ai_board_id)

    def get_new_history(self, count):
        """
        最新ヒストリーを取得
        :param count: int
        :rtype : list of AIBoardHistory
        """
        return list(AIBoardHistory.objects.filter(ai_board_id=self.ai_board_id).order_by('-version')[:count])