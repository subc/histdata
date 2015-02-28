# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import random

import django
from django.db import models, OperationalError
import time
from utils import ObjectField
from django.db import connection, connections
import traceback


class GeneticHistory(models.Model):
    """
    遺伝的アルゴリズムで交配した結果を記録する
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    generation = models.PositiveIntegerField(help_text='何世代目か')
    profit = models.IntegerField(default=0, help_text='利益')
    profit_max = models.IntegerField(default=0, help_text='最大利益')
    profit_min = models.IntegerField(default=0, help_text='最大損失')
    ai = ObjectField(null=True, default=None, help_text='aiのデータ')
    ai_id = models.PositiveIntegerField(null=True, default=None, help_text='AIのID')

    class Meta(object):
        app_label = 'genetic'

    @classmethod
    def record_history(cls, ai):
        # success = False
        # while not success:
        #     try:
        #         cls.objects.create(name=ai.name,
        #                            generation=ai.generation,
        #                            profit=ai.profit,
        #                            profit_max=ai.profit_max,
        #                            profit_min=ai.profit_min,
        #                            ai=ai.to_dict())
        #         success = True
        #     except OperationalError:
        #         print OperationalError
        #         print traceback.print_exc()
        #         django.db.close_old_connections()
        #         time.sleep(random.randint(1, 10))
        raise
        pass

    @classmethod
    def bulk_create_by_ai(cls, ai_group):
        objects = [cls.get_by_ai(ai) for ai in ai_group]
        cls.objects.bulk_create(objects)

    @classmethod
    def get_by_ai(cls, ai):
        return cls(name=ai.name,
                   generation=ai.generation,
                   profit=ai.profit,
                   profit_max=ai.profit_max,
                   profit_min=ai.profit_min,
                   ai=ai.ai_logic)


def re_connection():
    """
    wait_timeout対策
    バックグラウンドでループして動かすと、playerのshardはcommit_on_success外でコネクションが生きている可能性があるので
    カーソルを取り直すおまじないです
    """
    db_name = 'default'
    timeout = 36000
    con = connections[db_name].connection
    if con:
        cur = con.cursor()
    else:
        cur = connections[db_name].cursor()
    cur.execute('set session wait_timeout = {}'.format(timeout))


def re_connection2():
    connections['default'].cursor()


def re_connection3():
    import MySQLdb
    from django.conf import settings
    print settings.DATABASES
    db_settings = settings.DATABASES['default']
    connection = MySQLdb.connect(host=db_settings['HOST'], port=int(db_settings['PORT']), db=db_settings['NAME'],
                                 user=db_settings['USER'], passwd=db_settings['PASSWORD'])
    connection.stat()
    connection.cursor()