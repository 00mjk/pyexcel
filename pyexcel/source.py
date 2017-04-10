"""
    pyexcel.source
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Generic data source definition

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from lml.manager import Plugin

from pyexcel._compact import with_metaclass
import pyexcel.constants as constants


class Source(with_metaclass(Plugin, object)):
    """
    Define a data source for use with the signature functions

    This can be used to extend the function parameters once the custom
    class inherit this and register it with corresponding source registry
    """
    plugin_type = 'source'
    fields = [constants.SOURCE]
    attributes = []
    targets = []
    actions = []
    key = constants.SOURCE

    def __init__(self, **keywords):
        self._keywords = keywords

    def get_source_info(self):
        return (None, None)

    @classmethod
    def is_my_business(cls, action, **keywords):
        """
        If all required keys are present, this source is activated
        """
        statuses = [_has_field(field, keywords) for field in cls.fields]
        results = [status for status in statuses if status is False]
        return len(results) == 0

    def write_data(self, content):
        raise NotImplementedError("")

    def get_data(self):
        raise NotImplementedError("")


class MemorySourceMixin(object):

    def get_content(self):
        return self._content


def _has_field(field, keywords):
    return field in keywords and keywords[field] is not None
