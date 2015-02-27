# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import django
from django.db import models, OperationalError
from django.db.transaction import commit_on_success
from utils import ObjectField


class GeneticHistory(models.Model):
    """
    遺伝的アルゴリズムで交配した結果を記録する
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    generation = models.PositiveIntegerField(help_text='何世代目か')
    profit = models.IntegerField(default=0, help_text='利益')
    profit_max = models.IntegerField(default=0, help_text='最大利益')
    profit_min = models.IntegerField(default=0, help_text='最大損失')
    ai = ObjectField(null=True, default=None, help_text='aiのデータ')
    ai_id = models.PositiveIntegerField(null=True, default=None, help_text='AIのID')

    class Meta(object):
        app_label = 'genetic'

    @classmethod
    def record_history(cls, ai):
        success = False
        while not success:
            try:
                cls.objects.create(name=ai.name,
                                   generation=ai.generation,
                                   profit=ai.profit,
                                   profit_max=ai.profit_max,
                                   profit_min=ai.profit_min,
                                   ai=ai.to_dict())
                success = True
            except OperationalError:
                print OperationalError
                django.db.close_old_connections()
