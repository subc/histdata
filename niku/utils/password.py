# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


def get_password(key):
    """
    パスワードを応答する
    """
    try:
        from settings.passwd import Passwd
        return Passwd.get(key)
    except ImportError:
        return None