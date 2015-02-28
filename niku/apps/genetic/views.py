# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django import http
from apps.base.views import BasePostView
from module.genetic.models import GeneticHistory


class HistoryView(BasePostView):
    def post(self, request, params, *args, **kwargs):
        ai_group = []
        for ai in params.get('ai_group'):
            ai_group.append(AI(ai))
        GeneticHistory.bulk_create_by_ai(ai_group)
        return http.HttpResponse('1')


class AI(object):
    def __init__(self, params):
        self.params = params

    @property
    def name(self):
        return self.params.get('NAME')

    @property
    def generation(self):
        return int(self.params.get('GENERATION'))

    @property
    def profit(self):
        return int(self.params.get('PROFIT'))

    @property
    def profit_max(self):
        return int(self.params.get('PROFIT_MAX'))

    @property
    def profit_min(self):
        return int(self.params.get('PROFIT_MIN'))

    @property
    def ai_logic(self):
        return self.params.get('AI_LOGIC')

    @property
    def market(self):
        return self.params.get('MARKET')