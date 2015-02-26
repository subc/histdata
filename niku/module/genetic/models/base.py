# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


class CrossOverMixin(object):
    @classmethod
    def cross_over(cls, value_a, value_b):
        raise NotImplementedError