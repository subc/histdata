# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models
from utils import ObjectField


class OandaTransaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    oanda_time = models.DateTimeField()
    order_type = models.CharField(max_length=50, db_index=True)
    account_id = models.PositiveIntegerField(db_index=True)
    oanda_ticket_id = models.PositiveIntegerField(default=None, null=True, help_text='nullのときもある')
    _data = ObjectField(null=True, default=None, help_text='API応答の生データ')
