# -*- coding: utf-8 -*-
"""
Django標準adminのURLを試験する
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management import BaseCommand
import requests
from ...constans import TEST_HEADER, TEST_HOST


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.run()

    def run(self):
        url_base = 'http://{}/admin/'
        response = requests_api(url_base)
        assert response.status_code == 200, response.text


def requests_api(url_base, payload=None):
    url = url_base.format(TEST_HOST)
    if payload:
        response = requests.post(url, headers=TEST_HEADER, data=payload)
    else:
        response = requests.get(url, headers=TEST_HEADER)
    print 'URL SUCCESS: {}'.format(url)
    return response