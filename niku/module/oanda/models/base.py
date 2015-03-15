# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


class OandaAPIBase(object):
    def __init__(self, mode):
        """
        :param mode: OandaAPIMode
        """
        self.mode = mode


class OandaAPIModelBase(object):
    pass