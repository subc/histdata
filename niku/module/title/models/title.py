# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from utils.fixture import FakeModel


class TitleSettings(FakeModel):
    PUNK = 1
    fixtures = {
        PUNK: {
            'server': 'anago.2ch.net',
            'ita': 'applism',
            'keyword': 'ファントム',
        },
    }

    @property
    def _base(self):
        return 'http://{}/{}/'.format(self.sever, self.ita)

    @property
    def subject_url(self):
        """
        subject ファイル
        http://news22.2ch.net/newsplus/subject.txt
        :rtype: str
        """
        return self._base + 'subject.txt'

    @property
    def dat_url(self, filename):
        """
        dat ファイル
        http://news22.2ch.net/newsplus/dat/1185716060.dat
        :param filename:
        :rtype: str
        """
        return self._base + 'dat/{}'.format(filename)