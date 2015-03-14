# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
# from module.ai import get_ma_type


# class MAMixin(object):
#     def get_ratetype(self, open_bid, rates):
#         if rates[-1].ma is None:
#             return None
#
#         # keyの生成
#         l = []
#         ma = rates[-1].ma
#         for key in self.MA_KEYS:
#             ma_bid = getattr(ma, key)
#             if ma_bid is None:
#                 return None
#
#             l.append(str(get_ma_type(open_bid, ma_bid, self.base_tick_ma, rates[-1])))
#         key_value = ":".join(l)
#         return str('MA:{}'.format(key_value))
#
#     @property
#     def base_tick_ma(self):
#         return self.ai_dict['base_tick_ma']