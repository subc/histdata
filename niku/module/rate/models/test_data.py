# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
import pytz


class TestDataMixin(object):
    @classmethod
    def get_test_data(cls):
        return list(cls.objects.filter(start_at__gte=datetime.datetime(2010, 1, 1, tzinfo=pytz.utc)).order_by('start_at'))
