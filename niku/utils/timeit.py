# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from functools import wraps
import time


def timeit(fun=None):
    def _timeit(f):
        @wraps(f)
        def _inner(*args, **kwargs):
            ts = time.time()
            result = f(*args, **kwargs)
            te = time.time()
            # print u'task:{} args:[{}, {}] took: {} sec\n' \
            #       .format(f.__name__, args, kwargs, te-ts)
            print u'task:{} took: {} sec\n' \
                  .format(f.__name__, te-ts)
            return result

        return _inner

    return _timeit(fun) if fun else _timeit