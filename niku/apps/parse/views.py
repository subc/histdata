# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from datetime import datetime
from ..base.views import BaseView


class IndexView(BaseView):
    """
    index
    """
    template_name = "parse/index.html"

    def get(self, request, *args, **kwargs):
        csv_data = read_csv()
        # print csv_data
        print csv_data[1].to_text()
        return self.render_to_response({
            'chart_combo_data': "".join([x.to_text() for x in csv_data]),
            'chart_candle_data_single': csv_data[1].to_text(),
        })


class ParseView(BaseView):
    """
    parse
    """
    template_name = "parse/parse.html"

    def get(self, request, *args, **kwargs):
        csv_data = read_csv()
        return self.render_to_response({
        })


class CandleModel(object):
    """
    ろうそく単体
    """
    pt_open = 0 # 開始
    pt_close = 0 # 終了
    pt_high = 0 # その時間の最高値
    pt_low = 0 # その時間の最低値
    range_second = 0 # 何秒足のデータか
    start_at = None

    def __unicode__(self):
        return 'aaaaaaaa'

    @classmethod
    def load_from_histdata(cls, data_text, range_second):
        """
        histdata.netからのデータをロードする
        '20150213 165000;1.139140;1.139280;1.139140;1.139210;0'
        :param data_text: string
        :param range_second: int
        :rtype : CandleModel
        """
        # print "data is:", type(data_text), data_text
        r = data_text.split(';')
        assert(type(r) is list)
        assert(len(r)==6)

        obj = cls()
        obj.pt_open = float(r[1])
        obj.pt_close = float(r[4])
        obj.pt_high = float(r[2])
        obj.pt_low = float(r[3])
        obj.range_second = range_second
        obj.start_at = datetime(year=int(r[0][:4]),
                                month=int(r[0][4:6]),
                                day=int(r[0][6:8]),
                                hour=int(r[0][9:11]),
                                minute=int(r[0][11:13]))
        obj.self_check()
        return obj

    @property
    def name(self):
        return '{}:{}:{}'.format(self.start_at, self.pt_open, self.pt_close)

    def self_check(self):
        """
        自身の値が正しいかセルフチェックする
        """
        # 開始値が最高値と最低値の間にあること
        assert self.pt_high >= self.pt_open >= self.pt_low
        assert self.pt_high >= self.pt_close >= self.pt_low
        # 型チェック
        assert type(self.range_second) == int
        assert type(self.start_at) == datetime
        # 値チェック
        assert self.pt_high > 0
        assert self.pt_low > 0

    def to_text(self):
        """
        google chart用のjs_text変換

        例)
        ['Thu', 77, 77, 66, 50],

        最小
        オープン
        終了
        最大
        の順番です。
        """
        print "to_text --------------"
        print self.pt_high
        print self.pt_close
        return str("['" + \
               str(self.start_at) + "'," +\
               str(self.pt_low) + "," +\
               str(self.pt_open) + "," +\
               str(self.pt_close) + "," +\
               str(self.pt_high) + "," +\
               "],")


class HistDataModel(object):
    """
    為替データを扱う
    """
    def __init__(self):
        pass


def read_csv():
    """
    CSVを読む
    :rtype : list of CandleModel
    """
    import csv
    from django.conf import settings
    PATH = '{}/static/eur_usd/DAT_NT_EURUSD_M1_201502.csv'.format(settings.ROOT_PATH)
    csvdata=csv.reader(open(PATH, 'rb'), delimiter=str(','))

    r = []
    for data in csvdata:
        r.append(CandleModel.load_from_histdata(data[0], 60))
    return r
