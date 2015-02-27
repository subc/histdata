# -*- coding: utf-8 -*-
"""
Django settings for niku project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from .pathutil import abs_parent_path

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# プロジェクトのルートディレクトリパスを取得
ROOT_PATH = abs_parent_path(__file__, up_level=1)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%h%+$d&1&89l7g_wj!x5vi1z5r2%k^(o%7e!ggrqdol@^4_46='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'settings.urls'

WSGI_APPLICATION = 'wsgi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
NAME_PREFIX = 'fx'
DB_USER = 'root'
DB_PASS = ''
DB_HOST = '127.0.0.1'
DB_PORT = ''
CONN_MAX_AGE = 36000

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{}'.format(NAME_PREFIX),
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'CONN_MAX_AGE': CONN_MAX_AGE,
    },
}

DATABASE_OPTIONS = {
    "connect_timeout": CONN_MAX_AGE,
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

# International settings
LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Japan'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# 数字のカンマ区切りを何桁ごとに行うか
NUMBER_GROUPING = 3

# url.pyの場所
ROOT_URLCONF = 'urls'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


# 開発したモジュール
INSTALLED_APPS += (
    'south',
    'tests',
    'module.bbs',
    'module.trading',
    'module.rate',
    'module.genetic',
)

# テンプレート
TEMPLATE_DIRS = (
    ROOT_PATH + '/templates/',
)

# 静的ファイル
STATICFILES_DIRS = (
    './static/',
)

CACHE_BACKEND = 'locmem://'
