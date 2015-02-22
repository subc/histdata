# -*- coding: utf-8 -*-
"""
Django標準adminのURLを試験する
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from apps.parse.views import read_csv
from module.trading.models.trading import TradingManager
from utils.command import CustomBaseCommand


class Command(CustomBaseCommand):
    def handle(self, *args, **options):
        self.echo('処理開始')
        self.init()
        self.run()

    def init(self):
        self.csv_data = read_csv()

    def run(self):
        manager = TradingManager()
        rate_is_not_empty = True
        while rate_is_not_empty:
            # レート取得
            rate_is_not_empty = manager.get_rate()
            # print '現在のレート:', manager.current_rate.name

            # 既存ポジションを確認
            position = manager.sell()
            if position:
                self.echo('CLOSE! :open:{} close:{} 利益:¥{}'.format(position.open_rate.pt_open,
                                                                   position.close_rate.pt_open,
                                                                   position.get_profit()))

            # 新規ポジションを立てるか確認
            position = manager.buy()
            if position:
                self.echo('OPEN! :{}'.format(position.open_rate.pt_open))

            # 発注

            # 現在の利益の表示

            # 動き止める
            #time.sleep(1)

        # 結果
        self.echo('ただいまの利益:{}円 ポジション損益:{} ポジション数:{} 総取引回数:{}'.format(manager.profit_summary,
                                                                     manager.current_profit,
                                                                     len(manager.open_positions),
                                                                     len(manager.close_positions)))

        self.echo('処理終了')
