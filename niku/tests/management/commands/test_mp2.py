# -*- coding: utf-8 -*-
"""
マルチプロセスのテスト

# 参考
http://qiita.com/yubais/items/5a9d91fe03fe715b21d0
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import multiprocessing as mp
from module.genetic.models import GeneticHistory
from module.rate.models import CandleEurUsdH1Rate


L = 20000
proc = 8    # 8並列とする
h = hpy()

# 各プロセスが実行する計算
def f(p):  # p = 0,1,...,7
    # subtotal = 0
    #
    # # iの範囲を設定
    # ini = L * p / proc
    # fin = L * (p+1) / proc
    #
    # # 計算を実行
    # for i in range(ini, fin):
    #     for j in range(L):
    #         subtotal += i * j
    # print subtotal

    # DB書き込み試験
    GeneticHistory.objects.create(name='test_data',
                                  generation=1)
    print p
    return p


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        # 8個のプロセスを用意
        # pool = mp.Pool(proc)
        ct = 1

        while ct < 10:
            pool = mp.Pool(proc)

            # 各プロセスに subcalc(p) を実行させる
            # ここで p = 0,1,...,7
            # callbackには各戻り値がlistとして格納される
            callback = pool.map(f, range(20))

            print('---- Pool.map_async() (non-blocking) ----')
            print callback

            # 各戻り値の総和を計算
            total = sum(callback)

            ct += 1
            print "第{}世代完了! 結果:{}".format(ct, total)

            # pool内のワーカープロセスを停止する
            pool.close()
