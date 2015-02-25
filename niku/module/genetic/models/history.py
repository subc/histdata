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
    name = models.CharField()
    case = models.PositiveIntegerField()
    generation = models.PositiveIntegerField(help_text='何世代目か')
    profit = models.PositiveIntegerField(default=0, help_text='利益')
    profit_max = models.PositiveIntegerField(default=0, help_text='最大利益')
    profit_min = models.PositiveIntegerField(default=0, help_text='最大損失')
    ai = ObjectField(null=True, default=None, help_text='aiのデータ')