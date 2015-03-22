# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models
from utils import ObjectField


class OandaTransaction(models.Model):
    oanda_transaction_id = models.PositiveIntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    oanda_time = models.DateTimeField()
    order_type = models.CharField(max_length=50, db_index=True)
    account_id = models.PositiveIntegerField(db_index=True)
    oanda_trade_id = models.PositiveIntegerField(default=None, null=True, help_text='nullのときもある')
    _data = ObjectField(null=True, default=None, help_text='API応答の生データ')

    class Meta(object):
        app_label = 'oanda'

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
                            _data=t._data))
        if bulk:
            cls.objects.bulk_create(bulk)

    @classmethod
    def get_by_transaction_id(cls, oanda_transaction_id):
        try:
            return cls.objects.get(oanda_transaction_id=oanda_transaction_id)
        except cls.DoesNotExist:
            return None
