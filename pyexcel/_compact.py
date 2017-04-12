"""
    pyexcel._compact
    ~~~~~~~~~~~~~~~~~~~

    Compatibles

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
# flake8: noqa
import sys
import types
import warnings

PY2 = sys.version_info[0] == 2
PY26 = PY2 and sys.version_info[1] < 7

if PY26:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

if PY2:
    from StringIO import StringIO
    from StringIO import StringIO as BytesIO
    text_type = unicode
    exec('def reraise(tp, value, tb=None):\n raise tp, value, tb')
    class Iterator(object):
        def next(self):
            return type(self).__next__(self)
    import urllib2 as request
    irange = xrange
    from itertools import izip_longest as zip_longest
    from itertools import izip as czip
else:
    from io import StringIO, BytesIO
    text_type = str
    Iterator = object
    import urllib.request as request
    irange = range
    from itertools import zip_longest
    czip = zip
def is_tuple_consists_of_strings(an_array):
    return isinstance(an_array, tuple) and is_array_type(an_array, str)


def is_array_type(an_array, atype):
    tmp = [i for i in an_array if not isinstance(i, atype)]
    return len(tmp) == 0


def is_string(atype):
    """find out if a type is str or not"""
    if atype == str:
        return True
    elif PY2:
        if atype == unicode:
            return True
    return False


def is_generator(struct):
    return isinstance(struct, types.GeneratorType)


def deprecated(func, message="Deprecated!"):
    def inner(*arg, **keywords):
        warnings.warn(message, DeprecationWarning)
        return func(*arg, **keywords)
    return inner
