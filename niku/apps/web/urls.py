# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from .views import IndexView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'niku.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',  IndexView.as_view(), name='index'),
)
