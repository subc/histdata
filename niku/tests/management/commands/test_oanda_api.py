# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import requests
from ...constans import TEST_HEADER, TEST_HOST
from module.title.models.title import TitleSettings
from utils.oanda_api import OandaAPI, Streamer


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        api = OandaAPI(environment="sandbox", access_token=None, headers=None)
        api.get_prices()
        # Streamer().start()
        pass
