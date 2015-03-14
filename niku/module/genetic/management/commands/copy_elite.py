# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand, CommandError
import requests
from module.genetic.models import GeneticHistory, GeneticBackTestHistory
from module.rate import CurrencyPair


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        # eliteフラグ立てる
        for currency_pair in CurrencyPair:
            num = GeneticHistory.flag_elite(currency_pair.value)
            print 'COPY HISTORY:{}'.format(num)
        # バックテストにエリートを流し込む
        num = GeneticBackTestHistory.create_test_story()
        print "COPY ELITE COUNT:{}".format(num)
