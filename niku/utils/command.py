# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import datetime
import time


class CustomBaseCommand(BaseCommand):
    class Meta(object):
        abstract = True

    def echo(self, txt):
        """
        :param txt: string
        """
        # today()メソッドで現在日付・時刻のdatetime型データの変数を取得
        d = datetime.datetime.today()
        print d.strftime("%Y-%m-%d %H:%M:%S") + ':' + txt

    def check_kill_switch(self):
        """
        キルスイッチが有効か確認する
        """
        from module.account.models.kill_switch import KillSwitch
        if not KillSwitch.is_active():
            return
        self.echo('KILL SWITCH IS ACTIVE!! SLEEP 600 sec')
        time.sleep(600)
        self.echo('EXIT')
        exit()

    def critical_error(self, tag, e):
        """
        キルスイッチを有効にする
        :param tag: string
        :param e: Exception
        """
        self.echo('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        self.echo('CRITICAL ERROR')
        self.echo('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        from module.account.models.kill_switch import KillSwitch
        KillSwitch.create(tag, str(e))
        self.echo('CRITICAL KILL SWITCH ENABLE')