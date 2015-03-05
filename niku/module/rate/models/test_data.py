# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
import pytz


class TestDataMixin(object):
    @classmethod
    def get_test_data(cls):
        return list(cls.objects.filter(start_at__gte=datetime.datetime(2015, 2, 1, tzinfo=pytz.utc)).order_by('start_at'))

    @classmethod
    def get_test_data2(cls):
        return list(cls.objects.filter(start_at__gte=datetime.datetime(2012, 1, 1, tzinfo=pytz.utc)).order_by('start_at'))

    @classmethod
    def get_test_data3(cls):
        return list(cls.objects.filter(start_at__gte=datetime.datetime(2014, 1, 1, tzinfo=pytz.utc)).order_by('start_at'))

    @classmethod
    def get_test_data4(cls):
        return list(cls.objects.filter(start_at__gte=datetime.datetime(2015, 1, 1, tzinfo=pytz.utc)).order_by('start_at'))
