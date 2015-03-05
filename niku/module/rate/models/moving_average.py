# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.db import models
from .test_data import TestDataMixin


class MovingAverageBase(TestDataMixin, models.Model):
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

    KEYS = [
        'h1',
        'h4',
        'h24',
        'd5',
        'd10',
        'd25',
        'd75',
        'd200',
    ]

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
    def by_start_at(cls, start_at):
        """
        :param limit: int
        :rtype : list of MovingAverageBase
        """
        return cls.objects.filter(start_at__gte=start_at).order_by('start_at')

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
