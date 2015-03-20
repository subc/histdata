# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.db import models
import pytz
from .order import Order
from utils import ObjectField


class AIBoard(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    real = models.PositiveIntegerField(default=0, db_index=True)
    name = models.CharField(max_length=50)
    ai_id = models.PositiveIntegerField()
    ai_param = ObjectField(null=True, default=None, help_text='aiのデータ')
    currency_pair = models.PositiveIntegerField()
    account = models.PositiveIntegerField(null=True, default=None, help_text='OANDAのアカウントID')
    enable = models.PositiveIntegerField(db_index=True)
    memo = models.CharField(max_length=100)
    units = models.PositiveIntegerField(default=None, null=True, help_text='注文量')

    class Meta(object):
        app_label = 'board'


    @classmethod
    def get_all(cls):
        """
        :rtype : list of AIBoard
        """
        return list(cls.objects.filter())

    @classmethod
    def get_enable(cls):
        """
        :rtype : list of AIBoard
        """
        return list(cls.objects.filter(enable=1))

    def get_ai_instance(self):
        """
        :rtype : AI1EurUsd
        """
        from module.ai import get_ai_class_by
        return get_ai_class_by(self.ai_id).get_ai(self.ai_param,
                                                  self.name,
                                                  1,
                                                  self.ai_id)

    def get_oanda_api_mode(self):
        """
        :rtype : OandaAPIMode
        """
        from module.oanda.constants import OandaAPIMode
        if self.real:
            return OandaAPIMode.PRODUCTION
        return OandaAPIMode.DUMMY

    def can_order(self, prev_rate):
        """
        ポジション数による購入制限と時間による購入制限
        注文可能ならTrue
        :param prev_rate: Rate
        :rtype: bool
        """
        order = Order.get_new_order(self.id)

        # 初注文
        if order is None:
            return True

        # 前回レートと同じレートを参照しているなら発注不可
        if prev_rate:
            if order.prev_rate_at == prev_rate.start_at:
                return False

        # 時間制限
        now = datetime.datetime.now(pytz.utc)
        one_hours_ago = now - datetime.timedelta(seconds=3000)
        return one_hours_ago > order.created_at


class AICursor(models.Model):
    """
    AIがどの時間帯に注文を発したか
    """
    ai_board_id = models.PositiveIntegerField(db_index=True)
    time = models.DateTimeField(default=None, null=True)
    last_order_at = models.DateTimeField(default=None, null=True)

    class Meta(object):
        app_label = 'board'