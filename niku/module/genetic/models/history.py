# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import random

import django
from django.db import models, OperationalError
import time
from utils import ObjectField
from django.db import connection, connections
import traceback


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
    elite = models.PositiveIntegerField(null=True, default=None, help_text='優秀なAI')

    class Meta(object):
        app_label = 'genetic'

    @classmethod
    def get(cls, pk):
        return cls.objects.get(id=pk)

    @classmethod
    def bulk_create_by_ai(cls, ai_group):
        objects = [cls.get_by_ai(ai) for ai in ai_group]
        cls.objects.bulk_create(objects)

    @classmethod
    def get_by_ai(cls, ai):
        return cls(name=ai.name,
                   generation=ai.generation,
                   profit=ai.profit,
                   profit_max=ai.profit_max,
                   profit_min=ai.profit_min,
                   ai=ai.ai_logic)

    @classmethod
    def by_elite(cls):
        return list(cls.objects.filter(elite__gte=1))


class GeneticEliteHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    profitH1 = models.IntegerField(default=0, help_text='利益')
    profitH1_max = models.IntegerField(default=0, help_text='最大利益')
    profitH1_min = models.IntegerField(default=0, help_text='最大損失')
    profitM5 = models.IntegerField(default=0, help_text='利益')
    profitM5_max = models.IntegerField(default=0, help_text='最大利益')
    profitM5_min = models.IntegerField(default=0, help_text='最大損失')
    profitM1 = models.IntegerField(default=0, help_text='利益')
    profitM1_max = models.IntegerField(default=0, help_text='最大利益')
    profitM1_min = models.IntegerField(default=0, help_text='最大損失')
    genetic_id = models.PositiveIntegerField(null=True, default=None, help_text='GeneticHistoryに紐づくID', db_index=True)
    elite = models.PositiveIntegerField(null=True, default=None, help_text='優秀なAI')
    progress = models.CharField(max_length=50, help_text='進捗', null=True, default=None)

    class Meta(object):
        app_label = 'genetic'
        unique_together = ('genetic_id',)

    @classmethod
    def get_by_genetic(cls, genetic_id, for_update=False):
        if for_update:
            return cls.objects.select_for_update(genetic_id=genetic_id)
        return cls.objects.get(genetic_id=genetic_id)

    @classmethod
    def copy_by_history(cls):
        """
        GeneticHistoryから優秀なAIをコピーする
        :param genetic_id: int
        :rtype : int
        """
        elite_group = GeneticHistory.by_elite()

        # 登録済みデータは排除する
        genetic_ids = cls.get_genetic_ids()
        target = []
        for elite in elite_group:
            if elite.id not in genetic_ids:
                target.append(elite)
        # bulk!
        cls.objects.bulk_create([cls(name=x.name,
                                     profitH1=x.profit,
                                     profitH1_max=x.profit_max,
                                     profitH1_min=x.profit_min,
                                     genetic_id=x.id) for x in target])
        return len(target)

    @classmethod
    def get_genetic_ids(cls):
        return [x.genetic_id for x in cls.objects.filter()]

    @property
    def history(self):
        return GeneticHistory.get(self.genetic_id)