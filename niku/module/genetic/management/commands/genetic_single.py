# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import numpy
from module.genetic.models import Benchmark
from module.genetic.models.mixin import GeneticMixin, ApiMixin
from module.rate.models import CandleEurUsdH1Rate
from module.rate.models.eur import EurUsdMA
from module.ai import AI9EurUsd as AI
from .genetic import Command as CmdBase


class Command(CmdBase):
    # 最初の世代数
    AI_START_GENERATION = 1
    AI_START_NUM = 20
    AI_GROUP_SIZE = 20
    GENERATION_LIMIT = 300
    IS_SINGLE = True