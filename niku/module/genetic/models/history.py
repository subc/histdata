# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models
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
    elite = models.PositiveIntegerField(null=True, default=None, help_text='優秀なAI')
    currency_pair = models.PositiveIntegerField(default=0, help_text='通貨ペアID', db_index=True)

    class Meta(object):
        app_label = 'genetic'

    @classmethod
    def get(cls, pk):
        return cls.objects.get(id=pk)

    @classmethod
    def bulk_create_by_ai(cls, ai_group):
        # bulkで作ろうとしたら、2006エラーでるので１個づつ作る
        for ai in ai_group:
            cls.create_from_ai(ai)
        #
        # objects = [cls.create_from_ai(ai) for ai in ai_group]
        # for object in objects:
        #     object.save()
        # cls.objects.bulk_create(objects)

    @classmethod
    def create_from_ai(cls, ai):
        return cls.objects.create(name=ai.name,
                                  generation=ai.generation,
                                  profit=ai.profit,
                                  profit_max=ai.profit_max,
                                  profit_min=ai.profit_min,
                                  ai=ai.ai_logic,
                                  ai_id=ai.ai_id,
                                  currency_pair=ai.currency_pair)

    @classmethod
    def get_by_ai(cls, ai):
        return cls(name=ai.name,
                   generation=ai.generation,
                   profit=ai.profit,
                   profit_max=ai.profit_max,
                   profit_min=ai.profit_min,
                   ai=ai.ai_logic,
                   currency_pair=ai.currency_pair)

    @classmethod
    def by_elite(cls):
        return list(cls.objects.filter(elite__gte=1))
