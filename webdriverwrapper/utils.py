# -*- coding: utf-8 -*-

import six

__all__ = ('force_text',)


def force_text(value):
    if six.PY3:
        return str(value)
    if isinstance(value, str):
        return unicode(value, 'utf-8')
    return unicode(value)
