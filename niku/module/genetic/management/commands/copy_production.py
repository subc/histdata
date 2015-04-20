# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand, CommandError
import requests
from module.board.models import AIBoard
from module.genetic.models import GeneticHistory, GeneticBackTestHistory
from module.rate import CurrencyPair


class Command(BaseCommand):
    """
    rate dbにAIをコピーする
    """
    def handle(self, *args, **options):
        target_ids = [
31384,
32572,
33768,
34358,
60575,
126998,
128420,
143929,
165775,
166350,
167415,
168151,
169937,
172210,
174749,
175997,
176504,
177331,
195349,
197761,
197998,
277320,
278185,
306469,
306599,
306646,
306809,
306989,
307115,
307398,
307648,
307841,
307970,
308754,
308824,
308891,
308979,
309299,
309896,
310152,
310210,
310278,
310674,
310736,
311089,
311181,
311241,
311460,
312863,
313565,
313961,
315788,
331682,
345700,
364090,
366161,
366509,
368024,
368309,
370175,
371064,
372339,
372995,
373837,
374785,
376191,
376987,
377523,
385287]
        if target_ids:
            for _target_id in target_ids:
                self.run(_target_id, force=True)
        history_id = self._parse_args(args)
        self.run(history_id)

    def _parse_args(self, args):
        if len(args) != 1:
            raise CommandError(u'Usage: manage.py copy_production <ai_id>')
        history_id = int(args[0])

        return history_id

    def run(self, history_id, force=False):
        # インスタンス取得
        history = GeneticHistory.get(history_id)
        self.print_history(history)

        # 実行確認
        if force is False:
            print 'COPY START by push 1'
            input_data = input('>>>')
            if int(input_data) != 1:
                print 'FORCE EXIT!!'
                exit()

        # copy実行
        AIBoard.create(history, 'ID:{}'.format(history_id))

        # フラグ立てる
        GeneticBackTestHistory.set_elite(history_id)
        print 'COPY FINISH!!'

    def print_history(self, history):
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'AI LOGIC'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        for key in sorted(history.ai, key=lambda x: x):
            print '{}:{}'.format(key, history.ai[key])
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'AI_KEYS:{}'.format(len(history.ai))

        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'MARKET'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print history.ai.get('MARKET')

        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'STATUS'
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'