# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.functional import cached_property
import pytz
from .candle_type import CandleTypeMixin


class MovingAverageBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField(db_index=True, help_text='開始時間')
    h1 = models.FloatField(null=True, default=None)
    h4 = models.FloatField(null=True, default=None)
    h24 = models.FloatField(null=True, default=None)
    d5 = models.FloatField(null=True, default=None)
    d10 = models.FloatField(null=True, default=None)
    d25 = models.FloatField(null=True, default=None)
    d75 = models.FloatField(null=True, default=None)
    d200 = models.FloatField(null=True, default=None)

    class Meta(object):
        app_label = 'rate'
        abstract = True
        unique_together = ('start_at',)

    @classmethod
    def get_all(cls):
        """
        :return: list of MovingAverageBase
        """
        return list(cls.objects.filter())

    @classmethod
    def bulk_create(cls, objects):
        return cls.objects.bulk_create(objects)

    @classmethod
    def get_all_start_at(cls):
        """
        :rtype : list of datetime
        """
        return [obj.start_at for obj in cls.get_all()]


class EurUsdMA(MovingAverageBase):
    class Meta(object):
        app_label = 'rate'
        unique_together = ('start_at',)
