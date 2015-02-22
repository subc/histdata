# -*- coding: utf-8 -*-
"""
自作クラスの試験
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import requests
from ...constans import TEST_HEADER, TEST_HOST
from module.title.models.title import TitleSettings


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        CLS = [TitleSettings]
        for _c in CLS:
            _c.get_all()
