# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
from django.db import models
from module.rate import CurrencyPairToTable, Granularity
from .test_data import TestDataMixin


class MovingAverageBase(TestDataMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField(db_index=True, help_text='開始時間')
    open_bid = models.FloatField(null=True, default=None)
    h1 = models.FloatField(null=True, default=None)
    h4 = models.FloatField(null=True, default=None)
    h24 = models.FloatField(null=True, default=None)
    d5 = models.FloatField(null=True, default=None)
    d10 = models.FloatField(null=True, default=None)
    d25 = models.FloatField(null=True, default=None)
    d75 = models.FloatField(null=True, default=None)
    d200 = models.FloatField(null=True, default=None)
    # 水平線d25
    high_horizontal_d25 = models.FloatField(null=True, default=None)
    high_horizontal_d25_last_at = models.PositiveIntegerField(null=True, default=None, help_text='最安値から何日経過したか')
    low_horizontal_d25 = models.FloatField(null=True, default=None)
    low_horizontal_d25_last_at = models.PositiveIntegerField(null=True, default=None, help_text='最安値から何日経過したか')
    # 水平線d5
    high_horizontal_d5 = models.FloatField(null=True, default=None)
    high_horizontal_d5_last_at = models.PositiveIntegerField(null=True, default=None, help_text='最安値から何日経過したか')
    low_horizontal_d5 = models.FloatField(null=True, default=None)
    low_horizontal_d5_last_at = models.PositiveIntegerField(null=True, default=None, help_text='最安値から何日経過したか')

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

    class Meta(object):
        app_label = 'rate'
        abstract = True
        unique_together = ('start_at',)

    @classmethod
    def get_by_start_at(cls, start_at):
        """
        :param start_at: datetime
        :rtype : list of MovingAverageBase
        """
        try:
            return cls.objects.get(start_at=start_at)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_all(cls):
        """
        :return: list of MovingAverageBase
        """
        return list(cls.objects.filter())

    @classmethod
    def by_start_at(cls, start_at, count=None):
        """
        :param start_at: datetime
        :rtype : list of MovingAverageBase
        """
        if count:
            return list(cls.objects.filter(start_at__gte=start_at).order_by('start_at')[:count])
        return list(cls.objects.filter(start_at__gte=start_at).order_by('start_at'))

    @classmethod
    def bulk_create(cls, objects):
        return cls.objects.bulk_create(objects)

    @classmethod
    def get_all_start_at(cls):
        """
        :rtype : list of datetime
        """
        return [obj.start_at for obj in cls.get_all()]

    @classmethod
    def sync(cls, target_start_at, pair):
        """
        m5と同期する
        """
        m5_cls = CurrencyPairToTable.get_table(pair, Granularity.M5)
        m5_candles = m5_cls.by_start_at(target_start_at)
        ma_candles = cls.by_start_at(target_start_at)
        ma_start_at_list = [x.start_at for x in ma_candles]
        bulk = []
        for candle in m5_candles:
            if candle.start_at not in ma_start_at_list:
                # 登録
                bulk.append(cls.create_from_candle(candle, pair))
            # bulk!
            if len(bulk) > 3000:
                print 'bulk:{}'.format(pair)
                cls.objects.bulk_create(bulk)
                bulk = []
        # bulk!
        if bulk:
            cls.objects.bulk_create(bulk)

    @classmethod
    def create_from_candle(cls, candle, currency_pair):
        """
        5分足キャンドルからmaクラスを生成する。
        """
        _cls = cls(open_bid=candle.open_bid,
                   start_at=candle.start_at)
        _cls.set_ma(currency_pair)
        _cls.set_horizontal(currency_pair)
        return _cls

    def re_calc(self, currency_pair):
        """
        再計算して結果を調べる
        """
        import copy
        _copy_self = copy.deepcopy(self)
        _copy_self.set_ma(currency_pair)

        def ck(a, b):
            assert str(round(a, 5)) == str(round(b, 5)), '{}:{}'.format(a, b)
        ck(_copy_self.h1, self.h1)
        ck(_copy_self.h4, self.h4)
        ck(_copy_self.h24, self.h24)
        ck(_copy_self.d5, self.d5)
        ck(_copy_self.d10, self.d10)
        ck(_copy_self.d25, self.d25)
        ck(_copy_self.d75, self.d75)
        ck(_copy_self.d200, self.d200)

    def set_ma(self, currency_pair):
        """
        maをインスタンスに設定する
        """
        m5_cls = CurrencyPairToTable.get_table(currency_pair, Granularity.M5)
        d_cls = CurrencyPairToTable.get_table(currency_pair, Granularity.D)

        # h1
        self.h1 = get_avg(m5_cls.by_start_at(self.start_at - datetime.timedelta(seconds=60 * 60 + 5), count=12))

        # h4
        self.h4 = get_avg(m5_cls.by_start_at(self.start_at - datetime.timedelta(seconds=60 * 60 * 4 + 5), count=48))

        # h24
        self.h24 = get_avg(m5_cls.by_start_at(self.start_at - datetime.timedelta(seconds=60 * 60 * 24 + 5), count=288))

        # d5
        self.d5 = get_avg(d_cls.fuzzy_filter_between(self.start_at - datetime.timedelta(days=5+1),
                                                     self.start_at - datetime.timedelta(days=1)))

        # d10
        self.d10 = get_avg(d_cls.fuzzy_filter_between(self.start_at - datetime.timedelta(days=10+1),
                                                      self.start_at - datetime.timedelta(days=1)))

        # d25
        self.d25 = get_avg(d_cls.fuzzy_filter_between(self.start_at - datetime.timedelta(days=25+1),
                                                      self.start_at - datetime.timedelta(days=1)))

        # d75
        self.d75 = get_avg(d_cls.fuzzy_filter_between(self.start_at - datetime.timedelta(days=75+1),
                                                      self.start_at - datetime.timedelta(days=1)))

        # d200
        self.d200 = get_avg(d_cls.fuzzy_filter_between(self.start_at - datetime.timedelta(days=200+1),
                                                       self.start_at - datetime.timedelta(days=1)))

    def set_horizontal(self, currency_pair):
        """
        水平線をインスタンスに設定する
        """

        d_cls = CurrencyPairToTable.get_table(currency_pair, Granularity.D)

        # d5
        d5_candles = d_cls.fuzzy_filter_between(self.start_at - datetime.timedelta(days=5+1),
                                                self.start_at - datetime.timedelta(days=1))
        if len(d5_candles) > 2:
            high = max([x.high_bid for x in d5_candles])
            high_candle = [x for x in d5_candles if x.high_bid == high][0]
            high_diff = self.start_at - high_candle.start_at
            low = min([x.low_bid for x in d5_candles])
            low_candle = [x for x in d5_candles if x.low_bid == low][0]
            low_diff = self.start_at - low_candle.start_at

            self.high_horizontal_d5 = high
            self.high_horizontal_d5_last_at = high_diff.days
            self.low_horizontal_d5 = low
            self.low_horizontal_d5_last_at = low_diff.days

        # d25
        d25_candles = d_cls.fuzzy_filter_between(self.start_at - datetime.timedelta(days=25+1),
                                                 self.start_at - datetime.timedelta(days=1))
        if len(d25_candles) > 16:
            high = max([x.high_bid for x in d25_candles])
            high_candle = [x for x in d25_candles if x.high_bid == high][0]
            high_diff = self.start_at - high_candle.start_at
            low = min([x.low_bid for x in d25_candles])
            low_candle = [x for x in d25_candles if x.low_bid == low][0]
            low_diff = self.start_at - low_candle.start_at

            self.high_horizontal_d25 = high
            self.high_horizontal_d25_last_at = high_diff.days
            self.low_horizontal_d25 = low
            self.low_horizontal_d25_last_at = low_diff.days

    @property
    def d25_high_category(self):
        """
        最高値更新から、どれくらい経過したか
        """
        if self.high_horizontal_d25_last_at <= 13:
            return 'NEAR'
        else:
            return 'FAR'

    @property
    def d25_low_category(self):
        """
        最高値更新から、どれくらい経過したか
        """
        if self.low_horizontal_d25_last_at <= 13:
            return 'NEAR'
        else:
            return 'FAR'

    @property
    def d5_high_category(self):
        """
        最高値更新から、どれくらい経過したか
        """
        if self.high_horizontal_d5_last_at <= 3:
            return 'NEAR'
        else:
            return 'FAR'

    @property
    def d5_low_category(self):
        """
        最高値更新から、どれくらい経過したか
        """
        if self.low_horizontal_d5_last_at <= 3:
            return 'NEAR'
        else:
            return 'FAR'

    @property
    def key_category(self):
        return 'KEY-DAYS:D25:{}:{}:D5:{}:{}'.format(self.d25_high_category,
                                                    self.d25_low_category,
                                                    self.d5_high_category,
                                                    self.d5_low_category)

    @property
    def key_category_d5(self):
        return 'KEY-DAYS:D5:{}:{}'.format(self.d5_high_category,
                                          self.d5_low_category)

    @property
    def key_category_d25(self):
        return 'KEY-DAYS:D25:{}:{}'.format(self.d25_high_category,
                                           self.d25_low_category)


def get_avg(candles):
    return sum([x.close_bid for x in candles]) / float(len(candles))


class EurUsdMA(MovingAverageBase):
    class Meta(object):
        app_label = 'rate'
        unique_together = ('start_at',)
