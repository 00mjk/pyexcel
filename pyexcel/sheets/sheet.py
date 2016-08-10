"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Representation of data sheets

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .nominablesheet import NominableSheet, VALID_SHEET_PARAMETERS
from pyexcel.constants import (
    _IO_FILE_TYPE_DOC_STRING,
    _OUT_FILE_TYPE_DOC_STRING,
    DEFAULT_NAME
)
from pyexcel._compact import PY2


class Sheet(NominableSheet):
    """Two dimensional data container for filtering, formatting and iteration

    :class:`Sheet` is a container for a two dimensional array, where individual
    cell can be any Python types. Other than numbers, value of these
    types: string, date, time and boolean can be mixed in the array. This
    differs from Numpy's matrix where each cell are of the same number type.

    In order to prepare two dimensional data for your computation, formatting
    functions help convert array cells to required types. Formatting can be
    applied not only to the whole sheet but also to selected rows or columns.
    Custom conversion function can be passed to these formatting functions. For
    example, to remove extra spaces surrounding the content of a cell, a custom
    function is required.

    Filtering functions are used to reduce the information contained in the
    array.
    """
    def __init__(self, sheet=None, name=DEFAULT_NAME,
                 name_columns_by_row=-1,
                 name_rows_by_column=-1,
                 colnames=None,
                 rownames=None,
                 transpose_before=False,
                 transpose_after=False):
        """Constructor

        :param sheet: two dimensional array
        :param name: this becomes the sheet name.
        :param name_columns_by_row: use a row to name all columns
        :param name_rows_by_column: use a column to name all rows
        :param colnames: use an external list of strings to name the columns
        :param rownames: use an external list of strings to name the rows
        """
        NominableSheet.__init__(
            self,
            sheet=sheet,
            name=name,
            name_columns_by_row=name_columns_by_row,
            name_rows_by_column=name_rows_by_column,
            colnames=colnames,
            rownames=rownames,
            transpose_before=transpose_before,
            transpose_after=transpose_after
        )
        from pyexcel.sources import (get_sheet_rw_attributes,
                                     get_sheet_w_attributes)
        for attribute in get_sheet_rw_attributes():
            self.register_io(attribute)
        for attribute in get_sheet_w_attributes():
            self.register_presentation(attribute)

    class _RepresentedString:
        def __init__(self, text):
            self.text = text

        def __repr__(self):
            return self.text

        def __str__(self):
            return self.text

    @classmethod
    def register_presentation(cls, file_type):
        getter = presenter(file_type)
        file_type_property = property(
            getter,
            doc=_OUT_FILE_TYPE_DOC_STRING.format(file_type, "Sheet"))
        setattr(cls, file_type, file_type_property)
        setattr(cls, 'get_%s' % file_type, getter)

    @classmethod
    def register_io(cls, file_type):
        getter = presenter(file_type)
        setter = importer(file_type)
        file_type_property = property(
            getter, setter,
            doc=_IO_FILE_TYPE_DOC_STRING.format(file_type, "Sheet"))
        setattr(cls, file_type, file_type_property)
        setattr(cls, 'get_%s' % file_type, getter)
        setattr(cls, 'set_%s' % file_type, setter)

    def __repr__(self):
        return self.texttable

    def __str__(self):
        return self.texttable

    @property
    def content(self):
        """
        Plain representation without headers
        """
        content = self.get_texttable(write_title=False)
        return self._RepresentedString(content)

    def save_to(self, source):
        """Save to a writable data source"""
        source.write_data(self)

    def save_as(self, filename, **keywords):
        """Save the content to a named file

        Keywords may vary depending on your file type, because the associated
        file type employs different library.

        for csv, `fmtparams <https://docs.python.org/release/3.1.5/
        library/csv.html#dialects-and-formatting-parameters>`_ are accepted

        for xls, 'auto_detect_int', 'encoding' and 'style_compression' are
        supported

        for ods, 'auto_detect_int' is supported
        """
        import pyexcel.sources as sources
        out_source = sources.get_writable_source(
            file_name=filename, **keywords)
        return self.save_to(out_source)

    def save_to_memory(self, file_type, stream=None, **keywords):
        """Save the content to memory

        :param str file_type: any value of 'csv', 'tsv', 'csvz',
                              'tsvz', 'xls', 'xlsm', 'xlsm', 'ods'
        :param iostream stream: the memory stream to be written to. Note in
                                Python 3, for csv  and tsv format, please
                                pass an instance of StringIO. For xls, xlsx,
                                and ods, an instance of BytesIO.
        """
        get_method = getattr(self, "get_%s" % file_type)
        content = get_method(file_stream=stream, **keywords)
        return content

    def save_to_django_model(self,
                             model,
                             initializer=None,
                             mapdict=None,
                             batch_size=None):
        """Save to database table through django model

        :param model: a database model
        :param initializer: a initialization functions for your model
        :param mapdict: custom map dictionary for your data columns
        :param batch_size: a parameter to Django concerning the size
                           of data base set
        """
        import pyexcel.sources as sources
        source = sources.get_writable_source(
            model=model, initializer=initializer,
            mapdict=mapdict, batch_size=batch_size)
        self.save_to(source)

    def save_to_database(self, session, table,
                         initializer=None,
                         mapdict=None,
                         auto_commit=True):
        """Save data in sheet to database table

        :param session: database session
        :param table: a database table
        :param initializer: a initialization functions for your table
        :param mapdict: custom map dictionary for your data columns
        :param auto_commit: by default, data is committed.

        """
        import pyexcel.sources as sources
        source = sources.get_writable_source(
            session=session,
            table=table,
            initializer=initializer,
            mapdict=mapdict,
            auto_commit=auto_commit
        )
        self.save_to(source)


def presenter(file_type=None):
    def custom_presenter(self, **keywords):
        import pyexcel.sources as sources
        memory_source = sources.get_writable_source(file_type=file_type,
                                                    **keywords)
        self.save_to(memory_source)
        return memory_source.content.getvalue()
    return custom_presenter


def importer(file_type=None):
    def custom_presenter1(self, content, **keywords):
        from pyexcel.core import get_sheet_stream
        sheet_params = {}
        for field in VALID_SHEET_PARAMETERS:
            if field in keywords:
                sheet_params[field] = keywords.pop(field)
        named_content = get_sheet_stream(file_type=file_type,
                                         file_content=content,
                                         **keywords)
        self.init(named_content.payload,
                  named_content.name, **sheet_params)

    return custom_presenter1


def _one_sheet_tuple(items):
    if not PY2:
        items = list(items)
    return items[0][0], items[0][1]
