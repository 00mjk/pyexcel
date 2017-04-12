"""
    pyexcel.plugins.sources.output_to_memory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of output file sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel.internal import RENDERER
import pyexcel.constants as constants
from .file_sources import OutputSource
from . import params


# pylint: disable=W0223
class WriteSheetToMemory(OutputSource):
    fields = [params.FILE_TYPE]
    targets = (constants.SHEET,)
    actions = (constants.WRITE_ACTION,)
    attributes = RENDERER.get_all_file_types()

    def __init__(self, file_type=None, file_stream=None, **keywords):
        OutputSource.__init__(self, **keywords)

        self._renderer = RENDERER.get_a_plugin(file_type)
        if file_stream:
            self._content = file_stream
        else:
            self._content = self._renderer.get_io()
        self.attributes = RENDERER.get_all_file_types()

    def write_data(self, sheet):
        self._renderer.render_sheet_to_stream(
            self._content, sheet, **self._keywords)


# pylint: disable=W0223
class WriteBookToMemory(WriteSheetToMemory):
    """
    Multiple sheet data source for writting back to memory
    """
    targets = (constants.BOOK,)

    def write_data(self, book):
        self._renderer.render_book_to_stream(
            self._content, book, **self._keywords)
