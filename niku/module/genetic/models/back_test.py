# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
import pytz
from .history import GeneticHistory
from django.db import models, OperationalError
import time
from module.rate import CurrencyPair
from module.rate.consts import CURRENCY_PAIR_TO_TABLE
from module.rate.models.eur import Granularity, CandleEurUsdH1Rate
from utils import ObjectField


class GeneticBackTestHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    genetic_id = models.PositiveIntegerField(null=True, default=None, help_text='GeneticHistoryに紐づくID', db_index=True)
    currency_pair = models.PositiveIntegerField(default=0, help_text='通貨ペアID', db_index=True)
    name = models.CharField(max_length=50)
    profit = models.IntegerField(default=0, help_text='利益')
    profit_max = models.IntegerField(default=0, help_text='最大利益')
    profit_min = models.IntegerField(default=0, help_text='最大損失')
    elite = models.PositiveIntegerField(null=True, default=None, help_text='優秀なAI')
    test_start_at = models.DateTimeField(null=True, help_text='バックテストの開始期間')
    test_end_at = models.DateTimeField(null=True, help_text='バックテストの終了期間')
    span = models.IntegerField(default=0, help_text='キャンドル足の長さ')
    trade_count = models.IntegerField(default=None, null=True, help_text='取引回数')

    class Meta(object):
        app_label = 'genetic'
        unique_together = ('genetic_id', 'test_start_at', 'span')

    @classmethod
    def get(cls, pk):
        return cls.objects.get(id=pk)

    @classmethod
    def get_active(cls):
        """
        未試験のデータを返却
        :return: list of GeneticBackTestHistory
        """
        return list(cls.objects.filter(test_end_at=None))

    @classmethod
    def get_by_genetic(cls, genetic_id, for_update=False):
        if for_update:
            return cls.objects.select_for_update(genetic_id=genetic_id)
        return cls.objects.get(genetic_id=genetic_id)

    @classmethod
    def create_test_story(cls):
        """
        GeneticHistoryから優秀なAIをコピーして
        試験シナリオを生成する
        :rtype : int
        """
        elite_group = GeneticHistory.by_elite()

        # 登録済みデータは排除する
        genetic_ids = cls.get_genetic_ids()
        data = []
        for elite in elite_group:
            if elite.id not in genetic_ids:
                # 試験シナリオ生成
                data += cls.get_story(elite)

        # bulk!
        cls.objects.bulk_create(data)
        return len(data)

    @classmethod
    def get_story(cls, x):
        r = []
        t20100101 = datetime.datetime(2010, 1, 1, tzinfo=pytz.utc)
        t20120101 = datetime.datetime(2012, 1, 1, tzinfo=pytz.utc)
        t20140101 = datetime.datetime(2014, 1, 1, tzinfo=pytz.utc)
        t20150101 = datetime.datetime(2015, 1, 1, tzinfo=pytz.utc)
        # H1 2010/1/1〜
        r += [cls(name=x.name,
                  genetic_id=x.id,
                  currency_pair=x.currency_pair,
                  span=Granularity.H1.value,
                  test_start_at=t20100101)]
        # H1 2012/1/1〜
        r += [cls(name=x.name,
                  genetic_id=x.id,
                  currency_pair=x.currency_pair,
                  span=Granularity.H1.value,
                  test_start_at=t20120101)]
        # H1 2014/1/1〜
        r += [cls(name=x.name,
                  genetic_id=x.id,
                  currency_pair=x.currency_pair,
                  span=Granularity.H1.value,
                  test_start_at=t20140101)]
        # H1 2015/1/1〜
        r += [cls(name=x.name,
                  genetic_id=x.id,
                  currency_pair=x.currency_pair,
                  span=Granularity.H1.value,
                  test_start_at=t20150101)]
        # M5 2012/1/1〜
        r += [cls(name=x.name,
                  genetic_id=x.id,
                  currency_pair=x.currency_pair,
                  span=Granularity.M5.value,
                  test_start_at=t20120101)]
        # H1 2014/1/1〜
        r += [cls(name=x.name,
                  genetic_id=x.id,
                  currency_pair=x.currency_pair,
                  span=Granularity.M5.value,
                  test_start_at=t20140101)]
        # M5 2015/1/1〜
        r += [cls(name=x.name,
                  genetic_id=x.id,
                  currency_pair=x.currency_pair,
                  span=Granularity.M5.value,
                  test_start_at=t20150101)]
        # M1 2014/1/1〜
        r += [cls(name=x.name,
                  genetic_id=x.id,
                  currency_pair=x.currency_pair,
                  span=Granularity.M1.value,
                  test_start_at=t20140101)]
        # M1 2015/1/1〜
        r += [cls(name=x.name,
                  genetic_id=x.id,
                  currency_pair=x.currency_pair,
                  span=Granularity.M1.value,
                  test_start_at=t20150101)]
        return r

    @classmethod
    def get_genetic_ids(cls):
        return [x.genetic_id for x in cls.objects.filter()]

    @classmethod
    def result(cls, ai):
        """
        結果を更新する
        :param ai: AI
        """
        o = cls.get(ai.genetic_history_id)
        o.profit = ai.profit
        o.profit_max = ai.profit_max
        o.profit_min = ai.profit_min
        o.test_end_at = ai.end_at
        o.trade_count = ai.trade_count
        o.save()

    @property
    def history(self):
        return GeneticHistory.get(self.genetic_id)

    @property
    def candle_cls(self):
        return get_candle_cls(CurrencyPair(self.currency_pair), Granularity(self.span))


def get_candle_cls(currency_pair, granularity):
    """
    :param currency_pair:  CurrencyPair
    :param granularity: Granularity
    :rtype : Rate
    """
    return CURRENCY_PAIR_TO_TABLE.get(currency_pair).get(granularity)
