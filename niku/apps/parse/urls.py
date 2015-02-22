# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from .views import IndexView, ParseView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',  IndexView.as_view(), name='parse_index'),
    url(r'^parse/$',  ParseView.as_view(), name='parse_parse'),
)
