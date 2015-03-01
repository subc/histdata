# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from .views import HistoryView, HistoryEliteView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^history/$',  HistoryView.as_view(), name='history'),
    url(r'^history/elite$',  HistoryEliteView.as_view(), name='history_elite'),
)
