# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import pytz


def parse_time(time_text):
    """
    UTCの文字列をJSTへ変換する。
    例)
    2015-02-22T15:00:00.000000Z
    :param time_text: char
    :rtype : datetime
    """
    import datetime
    t = time_text
    # tt = [
    #     t[0:4],
    #     t[5:7],
    #     t[8:10],
    #     t[11:13],
    #     t[14:16],
    #     t[17:19],
    #     t[20:26],
    # ]
    # print tt
    utc = datetime.datetime(int(t[0:4]),
                            int(t[5:7]),
                            int(t[8:10]),
                            int(t[11:13]),
                            int(t[14:16]),
                            int(t[17:19]),
                            int(t[20:26]), tzinfo=pytz.utc)
    jst = utc.astimezone(pytz.timezone('Asia/Tokyo'))
    return jst
