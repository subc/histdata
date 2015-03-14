# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models
from utils import ObjectField


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

    @classmethod
    def get(cls, pk):
        return cls.objects.get(id=pk)

    @classmethod
    def bulk_create_by_ai(cls, ai_group):
        # bulkで作ろうとしたら、2006エラーでるので１個づつ作る
        for ai in ai_group:
            cls.create_from_ai(ai)
        #
        # objects = [cls.create_from_ai(ai) for ai in ai_group]
        # for object in objects:
        #     object.save()
        # cls.objects.bulk_create(objects)

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
    def flag_elite(cls):
        """
        500件の中からTOP1と2をエリートに設定する
        :return:
        """
        ct = 0
        for group in cls.get_history_by_n(500):
            if len(group) < 90:
                continue

            print 'TARGET:{} / {}'.format(group[0].id, cls.objects.all().order_by("-id")[0].id)
            sorted(group, key=lambda x: x.score, reverse=True)
            # スコアTOPにエリートフラグ付与
            group[0].set_elite()
            group[1].set_elite()
            ct += 2

            # それ以外にはノーマルフラグ立てる
            [history.set_normal() for history in group[2:]]
        return ct

    @classmethod
    def get_history_by_n(cls, n):
        """
        historyをn個のサブリストにして返却
        :param n: int
        :rtype : list of list of GeneticHistory
        """
        targets = cls.objects.filter(elite=None).order_by('id')
        return list(chunks(targets, n))

    def set_elite(self):
        self.elite = 1
        self.save()

    def set_normal(self):
        self.elite = 0
        self.save()


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]
