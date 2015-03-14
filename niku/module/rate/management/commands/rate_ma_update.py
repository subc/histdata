# -*- coding: utf-8 -*-
"""
レートに歯抜けがないかの観点でチェックする
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import copy
import datetime
from django.core.management import BaseCommand
from module.rate.models.eur import CandleEurUsdDRate, CandleEurUsdM5Rate, EurUsdMA
from module.rate.models.usd import CandleUsdJpyM5Rate, CandleUsdJpyDRate, UsdJpyMA


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        self.update_ma(UsdJpyMA, CandleUsdJpyM5Rate, CandleUsdJpyDRate)
        self.update_ma(EurUsdMA, CandleEurUsdM5Rate, CandleEurUsdDRate)

    def update_ma(self, cls_ma, cls_m5, cls_d1):
        write_history = cls_ma.get_all_start_at()
        candles_m5 = cls_m5.get_all()
        candles_d1 = cls_d1.get_all()
        self.write(cls_ma, write_history, candles_m5, candles_d1)

    def write(self, cls_ma, write_history, candles_m5, candles_d1):
        # 並び順番の試験
        prev = None
        for candle in candles_m5:
            if prev is None:
                prev = candle
                continue
            assert (prev.start_at < candle.start_at)
        prev = None
        for candle in candles_d1:
            if prev is None:
                prev = candle
                continue
            assert (prev.start_at < candle.start_at)

        # bulk!
        bulk = []
        index_max = len(candles_m5)
        for index in xrange(index_max):
            index = index_max - index - 1
            if index % 1000 == 0:
                print index, ' / ', index_max

            # 書き込み済みのときはスキップ
            if candles_m5[index].start_at in write_history:
                continue

            ma = self.calc_ma(index, candles_m5, candles_d1)
            bulk.append(copy.deepcopy(ma))

            # 3000毎に書き込み
            if len(bulk) > 3000:
                # 書き込み
                print "~~~~~~ bulk!! ~~~~~"
                cls_ma.bulk_create(bulk)

                # リセット
                bulk = []

        if bulk:
            cls_ma.bulk_create(bulk)


    def calc_ma(self, index, candles_m5, candles_d1):
        # ma計算
        ma = EurUsdMA(start_at=candles_m5[index].start_at)
        for key in KEYS:
            count = PAIR.get(key)
            candles = get_candles(count, index, candles_m5, candles_d1)
            if candles:
                setattr(ma, key, get_avg(candles))
        return ma


def get_avg(candles):
    return sum([x.close_bid for x in candles]) / float(len(candles))


def get_candles(count, index, candles_m5, candles_d1):
    if count >= 7200:
        # 5分毎のカウントを1日毎に変換
        count_d1 = count / 288
        # 25日平均以上は、1日足のデータを参照する
        return get_candles_d1(candles_d1, count_d1, candles_m5[index].start_at)
    else:
        return get_candles_m5(candles_m5, count, index)


def get_candles_d1(candles, count, start_at):
    _end_at = start_at - datetime.timedelta(days=1)
    _start_at = start_at - datetime.timedelta(days=1 + count)
    r = CandleEurUsdDRate.fuzzy_filter_between(_start_at, _end_at)
    # assert (count * 0.7 < len(r) <= count)
    if count * 0.7 < len(r) <= count:
        return r
    print
    return []


def get_candles_m5(candles, count, index):
    if 0 < index - count:
        target_candles = candles[index - count:index]
        assert len(target_candles) == count, str(len(target_candles)) + '/' + str(count)
        assert target_candles[-1].start_at < candles[index].start_at
        start_at = candles[index].start_at - datetime.timedelta(minutes=5*count)

        if target_candles[0].start_at == start_at:
            check(target_candles, start_at, candles[index].start_at)
            return target_candles

        if target_candles[0].start_at > start_at:
            for rev in xrange(0, index - count):
                rev = index - count - rev
                if candles[rev].start_at > start_at:
                    target_candles += [candles[rev]]
                else:
                    check(target_candles, start_at, candles[index].start_at)
                    return target_candles

        if target_candles[0].start_at < start_at:
            for rev in xrange(0, index - count):
                rev = index - count + rev
                if candles[rev].start_at < start_at:
                    target_candles.remove(candles[rev])
                else:
                    check(target_candles, start_at, candles[index].start_at)
                    return target_candles
    return []


def check(candles, start_at, end_at):
    pass
    # for c in candles:
    #     assert start_at <= c.start_at <= end_at, str(start_at) + ':::' + str(c.start_at) + ':::' + str(end_at) + \
    #                                             str([x.start_at for x in candles])

KEYS = [
    'h1',
    'h4',
    'h24',
    'd5',
    'd10',
    'd25',
    'd75',
    'd200',
]

PAIR = {
    'h1': 12,
    'h4': 48,
    'h24': 288,
    'd5': 1440,
    'd10': 2880,
    'd25': 7200,
    'd75': 21600,
    'd200': 57600,
}
