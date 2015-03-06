# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from .models import *


def get_ai_class_by(ai_id):
    d = {
        1: AI1EurUsd,
        2: AI2EurUsd,
        3: AI3EurUsd,
        4: AI4EurUsd,
        5: AI5EurUsd,
        6: AI6EurUsd,
    }
    ai_class = d.get(ai_id, None)
    if ai_class is None:
        raise ValueError, 'ai_class is None:{}'.format(ai_id)
    return ai_class