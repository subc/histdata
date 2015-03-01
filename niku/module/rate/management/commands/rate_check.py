# -*- coding: utf-8 -*-
"""
レートに歯抜けがないかの観点でチェックする
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
from module.rate.models.base import MultiCandles
from module.rate.models.eur import Granularity


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        # レート取得
        check(Granularity.D)
        # check(Granularity.H1)
        # check(Granularity.M5)


def check(granularity):
    """
    :param granularity: Granularity
    """
    for rates in generator(granularity):
        m = MultiCandles(rates)
        # print m.start_at, m.end_at
        print m.end_at - m.start_at, m.start_at


def generator(g):
    week_record_count = 5 * 24 * 3600 / g.value
    obj_all = g.db_table_class.get_all()
    r = []
    for index in xrange(0, len(obj_all) / week_record_count):
        yield obj_all[index * week_record_count: (index + 1) * week_record_count]
