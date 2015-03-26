# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models


class OandaOrderApiHistory(models.Model):
    """
    OrderAPIの接続履歴
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    units = models.IntegerField(default=None, null=True, help_text='注文量')
    _currency_pair = models.CharField(max_length=50, default=None, null=True)
    tag = models.CharField(max_length=50)
    response = models.TextField()

    class Meta(object):
        app_label = 'oanda'

    @classmethod
    def create(cls, response, units, pair, tag):
        cls.objects.create(response=response,
                           units=units,
                           _currency_pair=pair,
                           tag=tag)
