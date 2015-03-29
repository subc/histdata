# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models


class KillSwitch(models.Model):
    """
    連続取引状態に陥ったときに強制停止する
    有効になったら手動で切る運用
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_enable = models.BooleanField(default=True)
    tag = models.CharField(max_length=50)
    error_text = models.TextField()

    class Meta(object):
        app_label = 'account'

    @classmethod
    def create(cls, tag, error_text):
        cls.objects.create(tag=tag,
                           error_text=error_text)

    @classmethod
    def is_active(cls):
        """
        キルスイッチが有効ならTrue
        :rtype:
        """
        count = cls.objects.filter(is_enable=True).count()
        return count > 0