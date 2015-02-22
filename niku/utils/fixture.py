# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


def include(include_path):
    if include_path is None:
        return None

    module_path = '.'.join(include_path.split('.')[:-1])

    try:
        module = __import__(module_path)
    except ImportError:
        return None
    else:
        for path in include_path.split('.')[1:]:
            try:
                module = getattr(module, path)
            except AttributeError:
                return None

        return module


class FakeModelMeta(type):
    def __new__(mcls, name, bases, attrs):
        cls = type.__new__(mcls, name, bases, attrs)
        if name == 'FakeModel':
            return cls

        cls_module = cls.__module__
        if '.'.join(cls_module.split('.')[:1]) == "extension":
            cls_module = '.'.join(cls_module.split('.')[1:])

        excls = include('extension.%s.%s' % (cls_module, cls.__name__))

        if excls:
            cls.fixtures = excls.fixtures

        return cls


class FakeModel(object):
    __metaclass__ = FakeModelMeta

    fixtures = {}

    class DoesNotExist(Exception):
        pass

    def __init__(self, pk):
        fixture = self.fixtures.get(pk)

        if fixture is None:
            raise self.DoesNotExist(pk)

        for attr in ['pk', 'id']:
            setattr(self, attr, pk)

        for attr in fixture:
            setattr(self, attr, fixture[attr])

    @classmethod
    def get(cls, pk):
        return cls(pk)

    @classmethod
    def get_all(cls):
        return [cls(pk) for pk in cls.fixtures.iterkeys()]