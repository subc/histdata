# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
from module.oanda.models.api_price import PriceAPI


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        print 'order'
        # price取る
        PriceAPI.get_all()


        # AIインスタンス生成

        # 仮注文発砲

        # API注文

        # 注文成立したあと
