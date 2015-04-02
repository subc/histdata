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
        7: AI7EurUsd,
        9: AI9EurUsd,
        10: AI10EurUsd,
        11: AI11EurUsd,
        1001: AI1001UsdJpy,
        1002: AIHoriUsdJpy1002,
        2001: AI2001Gbp,
        3001: AI3001Aud,
    }
    ai_class = d.get(ai_id, None)
    if ai_class is None:
        raise ValueError, 'ai_class is None:{}'.format(ai_id)
    return ai_class