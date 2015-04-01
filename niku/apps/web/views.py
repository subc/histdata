# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from ..base.views import BaseView
from module.oanda.constants import OandaAPIMode
from module.oanda.models.api_account import AccountAPI


class IndexView(BaseView):
    """
    アカウント情報のサマリーページ
    """
    template_name = "web/index.html"

    def get(self, request, *args, **kwargs):
        account = AccountAPI(OandaAPIMode.PRODUCTION, 6181277).get_all()
        return self.render_to_response({
            'account': account,
        })