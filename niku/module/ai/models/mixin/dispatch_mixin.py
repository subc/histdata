# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


class DispatchMixin(object):
    def _dispatch(self):
        if 'depth' not in self.ai_dict:
            self.ai_dict['depth'] = 24
        if 'base_tick_ma' not in self.ai_dict:
            self.ai_dict['base_tick_ma'] = 50
        # AI7 横横のときの売買基準
        if 'yokoyoko_base_tcik' not in self.ai_dict:
            self.ai_dict['yokoyoko_base_tcik'] = 20

        # AI7 上げ下げ相場の判断基準
        if 'up_down_base_tick' not in self.ai_dict:
            self.ai_dict['up_down_base_tick'] = 70

    @property
    def depth(self):
        return self.ai_dict['depth']

    @property
    def base_tick_ma(self):
        return self.ai_dict['base_tick_ma']

    @property
    def yokoyoko_base_tcik(self):
        return self.ai_dict['yokoyoko_base_tcik']

    @property
    def up_down_base_tick(self):
        return self.ai_dict['up_down_base_tick']