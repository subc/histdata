# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import numpy
from module.genetic.models.benchmark_single import BenchmarkSingle
from module.genetic.models.mixin import GeneticMixin, ApiMixin
# from module.ai import AI1001UsdJpy as AI
# from module.ai import AI2001Gbp as AI
from module.ai import AIMarketTimeAudUsd3002 as AI
from .genetic_single import Command as CMD


class Command(CMD):
    @property
    def ai_class(self):
        return AI
    

def get_ai_group(ai_class, suffix, num, generation):
    """
    :rtype : list of AI
    """
    base_ai = ai_class({}, suffix, generation)
    return base_ai.initial_create(num)
