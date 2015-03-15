# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_at = models.DateTimeField(default=None, null=True)
    end_at = models.DateTimeField(default=None, null=True, db_index=True)
    oanda_ticket_id = models.PositiveIntegerField(default=None, null=True)
    ai_board_id = models.PositiveIntegerField()
    currency_pair = models.PositiveIntegerField()
    buy = models.PositiveIntegerField()
    spread = models.FloatField()
    open_rate = models.FloatField(default=None, null=True, help_text='想定注文レート')
    real_open_rate = models.FloatField(default=None, null=True, help_text='約定時の注文レート')
    limit_rate = models.FloatField()
    stop_limit_rate = models.FloatField()
    real_limit_rate = models.FloatField(default=None, null=True, help_text='約定時の注文レート')
    real = models.PositiveIntegerField(default=0, db_index=True)
    profit = models.PositiveIntegerField(default=0, null=True)

    class Meta(object):
        app_label = 'board'