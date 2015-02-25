# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import msgpack
import base64
from django.db import models


class _AddInstrospectionRulesMixin(object):
    def add_to_introspection_rule(self):
        try:
            from south.modelsinspector import add_introspection_rules
        except ImportError:
            pass
        else:
            cls_name = '.'.join([self.__module__, self.__class__.__name__])
            regex_str = '^' + cls_name.replace('.', '\\.')
            add_introspection_rules(
                [([self.__class__], [], {}), ],
                [regex_str])


class ObjectField(models.Field, _AddInstrospectionRulesMixin):
    description = u'msgpack'

    __metaclass__ = models.SubfieldBase

    def __init__(self,
                 packb_kwargs={}, unpackb_kwargs={},
                 *args, **kwargs):
        self.add_to_introspection_rule()
        self._packb_kwargs = packb_kwargs
        self._unpackb_kwargs = unpackb_kwargs
        super(ObjectField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def to_python(self, value):
        if value is None:
            return value
        if not type(value) in [str, unicode]:
            return value
        return msgpack.unpackb(base64.b64decode(value), **self._unpackb_kwargs)

    def get_db_prep_save(self, value, connection):
        if value is None:
            return
        return base64.b64encode(msgpack.packb(value, **self._packb_kwargs))