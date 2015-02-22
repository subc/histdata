# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from ..base.views import BaseView


class IndexView(BaseView):
    template_name = "web/index.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})