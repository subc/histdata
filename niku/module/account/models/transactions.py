# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.db import models
import pytz
from utils import ObjectField


class OandaTransaction(models.Model):
    oanda_transaction_id = models.PositiveIntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    oanda_time = models.DateTimeField()
    order_type = models.CharField(max_length=50, db_index=True)
    account_id = models.PositiveIntegerField(db_index=True)
    oanda_trade_id = models.PositiveIntegerField(default=None, null=True, help_text='nullのときもある')
    accountBalance = models.FloatField(default=None, null=True, help_text='現在時点の口座資金')
    memo = models.CharField(max_length=50, default=None, null=True)
    pl = models.FloatField(default=None, null=True, help_text='ポジション決済時の実現損益')
    _data = ObjectField(null=True, default=None, help_text='API応答の生データ')

    class Meta(object):
        app_label = 'account'

    @classmethod
    def bulk_write(cls, account_id, oanda_transactions):
        """
        :param oanda_transactions: list of TransactionsAPIModel
        """
        bulk = []
        for t in oanda_transactions:
            obj = cls.get_by_transaction_id(t.oanda_transaction_id)
            if obj:
                continue

            bulk.append(cls(oanda_transaction_id=t.oanda_transaction_id,
                            oanda_time=t.time,
                            account_id=account_id,
                            oanda_trade_id=t.tradeId,
                            order_type=t.order_type,
                            _data=t._data,
                            accountBalance=t.accountBalance,
                            pl=t.profit,
                            memo=t.memo))
        if bulk:
            cls.objects.bulk_create(bulk)

    @classmethod
    def get_by_transaction_id(cls, oanda_transaction_id):
        try:
            return cls.objects.get(oanda_transaction_id=oanda_transaction_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_market_order_count(cls, seconds=3600):
        """
        N秒前から何回マーケットオーダーが行われたか回数を返却
        :param seconds: int
        """
        now = datetime.datetime.now(tz=pytz.utc)
        one_hours_later = now - datetime.timedelta(seconds=3600)
        count = cls.objects.filter(order_type='MARKET_ORDER_CREATE',
                                   created_at__gte=one_hours_later).count()
        return count
