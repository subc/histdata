# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.db import models
import pytz
from module.account.models import Order
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
    version = models.PositiveIntegerField(default=1, null=True, help_text='AIの取引世代')

    class Meta(object):
        app_label = 'board'

    @classmethod
    def get(cls, pk):
        return cls.objects.get(id=pk)

    @classmethod
    def get_all(cls):
        """
        :rtype : list of AIBoard
        """
        return list(cls.objects.filter(enable=1))

    @classmethod
    def get_enable_and_main(cls):
        return list(cls.objects.filter(units__gt=1, enable=1))

    @classmethod
    def get_accounts(cls):
        """
        アカウント一覧を返却
        :rtype : list of AIBoard
        """
        qs = cls.objects.filter()
        qs.query.group_by = ['account']
        return [obj.account for obj in list(qs)]

    @classmethod
    def create(cls, history, memo, account=6181277):
        cls.objects.using('rate').create(real=1,
                                         name=history.name,
                                         ai_id=history.ai_id,
                                         ai_param=history.ai,
                                         currency_pair=history.currency_pair,
                                         account=account,
                                         enable=1,
                                         units=1,
                                         version=1,
                                         memo=memo)

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

        # ポジション数制限
        position_num = Order.get_position_count(self.id)
        if position_num > 9:
            return False

        # 時間制限
        now = datetime.datetime.now(pytz.utc)
        one_hours_ago = now - datetime.timedelta(seconds=3600)
        print one_hours_ago, order.created_at, one_hours_ago > order.created_at
        return one_hours_ago > order.created_at

    def update_units(self, history):
        """
        取引量を変更
        :param history: AIBoardHistory
        """
        self.units = history.after_units
        self.version_up()
        self.save()

    def version_up(self):
        self.version += 1

    def trade_stop(self):
        """
        取引停止を記録
        """
        self.enable = 0
        self.save()