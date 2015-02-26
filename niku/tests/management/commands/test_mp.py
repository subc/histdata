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

L = 20000
proc = 4    # 8並列とする

# 各プロセスが実行する計算
def subcalc(p):  # p = 0,1,...,7
    subtotal = 0

    # iの範囲を設定
    ini = L * p / proc
    fin = L * (p+1) / proc

    # 計算を実行
    for i in range(ini, fin):
        for j in range(L):
            subtotal += i * j
    return subtotal


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
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