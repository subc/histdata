# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import datetime


class CustomBaseCommand(BaseCommand):
    def echo(self, txt):
        """
        :param txt: string
        """
        # today()メソッドで現在日付・時刻のdatetime型データの変数を取得
        d = datetime.datetime.today()
        print d.strftime("%Y-%m-%d %H:%M:%S") + ':' + txt
