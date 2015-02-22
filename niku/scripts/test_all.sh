#!/bin/bash
# エラーなら停止
set -e
cd `dirname $0`/../

# 初期化

# 開発した機能の試験
python ./manage.py test_fakemodel
python ./manage.py test_admin
python ./manage.py test_web
python ./manage.py test_parse
