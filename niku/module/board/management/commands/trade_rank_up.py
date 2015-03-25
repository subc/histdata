# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import time
from module.board.models import AIBoard, AIBoardHistory


class Command(BaseCommand):
    """
    取引量を変化させる
    """

    def handle(self, *args, **options):
        self.run()
        time.sleep(120)

    def run(self):
        # 取引量変化
        boards = AIBoard.get_all()
        history_group = []
        for board in boards:
            history = AIBoardHistory.create_if_achieve(board)
            if history:
                # 取引量の更新
                board.update_units(history)
                history_group.append(history)

        # 取引停止
        for history in history_group:
            if not history.is_rank_up:
                if history.check_tarade_stop():
                    history.trade_stop()