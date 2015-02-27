# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import time
from utils.timeit import timeit
from django.core.management import BaseCommand
import multiprocessing as mp

L = 20000
proc = 4    # 8並列とする


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        # シングルスレッド
        # for x in xrange(10):
        #     TestSpeed.sleep()

        # マルチスレッド
        # 8個のプロセスを用意
        pool = mp.Pool(proc)

        # 各プロセスに subcalc(p) を実行させる
        # ここで p = 0,1,...,7
        # callbackには各戻り値がlistとして格納される
        callback = pool.map(subcalc, range(8))

        print('---- Pool.map_async() (non-blocking) ----')
        print callback

        # 各戻り値の総和を計算
        total = sum(callback)

        print (total)


class TestSpeed(object):
    CACHE = None

    @classmethod
    @timeit
    def sleep(cls):
        if cls.CACHE:
            return cls.CACHE
        time.sleep(3)
        cls.CACHE = 1
        return 1


# 各プロセスが実行する計算
def subcalc(p):
    print p
    TestSpeed.sleep()
    return 1