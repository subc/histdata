# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models
from utils import ObjectField


class AIBoard(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    real = models.PositiveIntegerField(default=0, db_index=True)
    name = models.CharField(max_length=50)
    ai_id = models.PositiveIntegerField()
    ai_param = ObjectField(null=True, default=None, help_text='aiのデータ')
    currency_pair = models.PositiveIntegerField()
    enable = models.PositiveIntegerField(db_index=True)
    memo = models.CharField(max_length=100)

    class Meta(object):
        app_label = 'board'

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


class AICursor(models.Model):
    """
    AIがどの時間帯に注文を発したか
    """
    ai_board_id = models.PositiveIntegerField(db_index=True)
    time = models.DateTimeField(default=None, null=True)
    last_order_at = models.DateTimeField(default=None, null=True)

    class Meta(object):
        app_label = 'board'