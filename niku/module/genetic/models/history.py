# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models
from utils import ObjectField
from utils.timeit import timeit


class GeneticHistory(models.Model):
    """
    遺伝的アルゴリズムで交配した結果を記録する
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    generation = models.PositiveIntegerField(help_text='何世代目か')
    score = models.IntegerField(default=0, help_text='AIの性能', db_index=True)
    profit = models.IntegerField(default=0, help_text='利益', db_index=True)
    profit_max = models.IntegerField(default=0, help_text='最大利益')
    profit_min = models.IntegerField(default=0, help_text='最大損失')
    ai = ObjectField(null=True, default=None, help_text='aiのデータ')
    ai_id = models.PositiveIntegerField(null=True, default=None, help_text='AIのID')
    elite = models.IntegerField(db_index=True, null=True, default=None, help_text='優秀なAI')
    currency_pair = models.PositiveIntegerField(default=0, help_text='通貨ペアID', db_index=True)

    class Meta(object):
        app_label = 'genetic'
        unique_together = (
            # eliteとcurrency_pairで検索するのでINDEXつくっておく
            ('id', 'elite', 'currency_pair'),
            ('id', 'ai_id', 'elite', 'currency_pair'),
        )

    @classmethod
    def get(cls, pk):
        return cls.objects.get(id=pk)

    @classmethod
    def bulk_create_by_ai(cls, ai_group):
        # bulkで作ろうとしたら、2006エラーでるので１個づつ作る
        for ai in ai_group:
            cls.create_from_ai(ai)

    @classmethod
    def create_from_ai(cls, ai):
        return cls.objects.create(name=ai.name,
                                  generation=ai.generation,
                                  score=ai.score,
                                  profit=ai.profit,
                                  profit_max=ai.profit_max,
                                  profit_min=ai.profit_min,
                                  ai=ai.ai_logic,
                                  ai_id=ai.ai_id,
                                  currency_pair=ai.currency_pair)

    @classmethod
    def get_by_ai(cls, ai):
        return cls(name=ai.name,
                   generation=ai.generation,
                   profit=ai.profit,
                   profit_max=ai.profit_max,
                   profit_min=ai.profit_min,
                   ai=ai.ai_logic,
                   currency_pair=ai.currency_pair)

    @classmethod
    def by_elite(cls):
        return list(cls.objects.filter(elite__gte=1))

    @classmethod
    def flag_elite(cls, currency_pair_id):
        """
        1000件の中からTOP1と2をエリートに設定する
        :param currency_pair_id: int
        :return:
        """
        for x in xrange(3):
            print 'categorize'
            cls.categorize(cls.get_history_by_n(1000, currency_pair_id))

    @classmethod
    def categorize(cls, group):
        """
        :param group: list of cls
        """
        if len(group) < 900:
            return

        group = sorted(group, key=lambda x: x.score, reverse=True)

        # スコアTOPにエリートフラグ付与
        group[0].set_elite()
        group[1].set_elite()
        group[2].set_elite()
        group[3].set_elite()
        group[4].set_elite()

        # それ以外にはノーマルフラグ立てる
        [history.set_normal() for history in group[5:]]
        return 5

    @classmethod
    @timeit
    def get_history_by_n(cls, n, currency_pair_id):
        """
        historyをn個のサブリストにして返却
        :param n: int
        :param currency_pair_id: int
        :rtype : list of list of GeneticHistory
        """
        return list(cls.objects.filter(elite=None, currency_pair=currency_pair_id)[:n])

    def set_elite(self):
        self.elite = 1
        self.save()

    def set_normal(self):
        self.elite = 0
        self.save()


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]
