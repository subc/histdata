# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.views.generic import View, TemplateView
import ujson


class BaseView(TemplateView):
    pass


class BasePostView(View):
    """
    sample

    def post(self, request, params, *args, **kwargs):
    """
    def dispatch(self, request, *args, **kwargs):
        body = dict(request.POST.iterlists())
        params = ujson.loads(body.get('data')[0])
        return super(BasePostView, self).dispatch(request, params=params, *args, **kwargs)