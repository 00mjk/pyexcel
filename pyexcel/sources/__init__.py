# flake8: noqa
from . import file_source_output, database
from . import file_source_input, http, pydata
from . import factory
from pyexcel._compact import PY2
from pyexcel.generators import BookStream, SheetStream
import pyexcel.constants as constants
from functools import partial


def get_sheet_stream(**keywords):
    source = factory.get_source(**keywords)
    sheets = source.get_data()
    sheet_name, data = one_sheet_tuple(sheets.items())
    return SheetStream(sheet_name, data)


def get_book_stream(**keywords):
    """Get an instance of :class:`Book` from an excel source

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    source = factory.get_book_source(**keywords)
    sheets = source.get_data()
    filename, path = source.get_source_info()
    book = BookStream(sheets, filename=filename, path=path)
    return book


def save_sheet(sheet, **keywords):
    source = factory.get_writable_source(**keywords)
    source.write_data(sheet)
    if hasattr(source, 'content'):
        _try_put_file_read_pointer_to_its_begining(source.content)
        return source.content


def save_book(book, **keywords):
    source = factory.get_writable_book_source(**keywords)
    source.write_data(book)
    if hasattr(source, 'content'):
        _try_put_file_read_pointer_to_its_begining(source.content)
        return source.content


class SheetMixin:
    @classmethod
    def init_attributes(cls):
        for attribute in factory.get_sheet_rw_attributes():
            cls.register_io(attribute)
        for attribute in factory.get_sheet_w_attributes():
            cls.register_presentation(attribute)

    @classmethod
    def register_presentation(cls, file_type):
        getter = presenter(file_type)
        file_type_property = property(
            getter,
            doc=constants._OUT_FILE_TYPE_DOC_STRING.format(file_type, "Sheet"))
        setattr(cls, file_type, file_type_property)
        setattr(cls, 'get_%s' % file_type, getter)

    @classmethod
    def register_io(cls, file_type):
        getter = presenter(file_type)
        setter = importer(file_type)
        file_type_property = property(
            getter, setter,
            doc=constants._IO_FILE_TYPE_DOC_STRING.format(file_type, "Sheet"))
        setattr(cls, file_type, file_type_property)
        setattr(cls, 'get_%s' % file_type, getter)
        setattr(cls, 'set_%s' % file_type, setter)

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
        return save_sheet(self, file_name=filename,
                          **keywords)

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
        save_sheet(self,
                   model=model, initializer=initializer,
                   mapdict=mapdict, batch_size=batch_size)


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
        save_sheet(self,
                   session=session,
                   table=table,
                   initializer=initializer,
                   mapdict=mapdict,
                   auto_commit=auto_commit
               )


def register_presentation(cls, file_type):
    getter = book_presenter(file_type)
    file_type_property = property(
        getter,
        doc=constants._OUT_FILE_TYPE_DOC_STRING.format(file_type, "Book"))
    setattr(cls, file_type, file_type_property)
    setattr(cls, 'get_%s' % file_type, getter)


def register_io(cls, file_type):
    getter = book_presenter(file_type)
    setter = book_importer(file_type)
    file_type_property = property(
        getter, setter,
        doc=constants._IO_FILE_TYPE_DOC_STRING.format(file_type, "Book"))
    setattr(cls, file_type, file_type_property)
    setattr(cls, 'get_%s' % file_type, getter)
    setattr(cls, 'set_%s' % file_type, setter)


class BookMeta(type):
    def __init__(cls, name, bases, nmspc):
        super(BookMeta, cls).__init__(name, bases, nmspc)
        for attribute in factory.get_book_rw_attributes():
            register_io(cls, attribute)
        for attribute in factory.get_book_w_attributes():
            register_presentation(cls, attribute)


class BookMixin(object):
    @classmethod
    def register_presentation(cls, file_type):
        register_presentation(cls, file_type)

    @classmethod
    def register_io(cls, file_type):
        register_io(cls, file_type)

    def save_as(self, filename):
        """Save the content to a new file

        :param str filename: a file path
        """
        return save_book(self, file_name=filename)

    def save_to_memory(self, file_type, stream=None, **keywords):
        """Save the content to a memory stream

        :param file_type: what format the stream is in
        :param stream: a memory stream.  Note in Python 3, for csv and tsv
                       format, please pass an instance of StringIO. For xls,
                       xlsx, and ods, an instance of BytesIO.
        """
        get_method = getattr(self, "get_%s" % file_type)
        content = get_method(file_stream=stream, **keywords)
        return content

    def save_to_django_models(self, models,
                              initializers=None, mapdicts=None,
                              batch_size=None):
        """Save to database table through django model

        :param models: a list of database models, that is accepted by
                       :meth:`Sheet.save_to_django_model`. The sequence
                       of tables matters when there is dependencies in
                       between the tables. For example, **Car** is made
                       by **Car Maker**. **Car Maker** table should be
                       specified before **Car** table.
        :param initializers: a list of intialization functions for your
                             tables and the sequence should match tables,
        :param mapdicts: custom map dictionary for your data columns
                         and the sequence should match tables
        """
        save_book(self,
                  models=models,
                  initializers=initializers,
                  mapdicts=mapdicts,
                  batch_size=batch_size)

    def save_to_database(self, session, tables,
                         initializers=None, mapdicts=None,
                         auto_commit=True):
        """Save data in sheets to database tables

        :param session: database session
        :param tables: a list of database tables, that is accepted by
                       :meth:`Sheet.save_to_database`. The sequence of tables
                       matters when there is dependencies in between the
                       tables. For example, **Car** is made by **Car Maker**.
                       **Car Maker** table should
                       be specified before **Car** table.
        :param initializers: a list of intialization functions for your
                             tables and the sequence should match tables,
        :param mapdicts: custom map dictionary for your data columns
                         and the sequence should match tables
        :param auto_commit: by default, data is committed.

        """
        save_book(self,
                  session=session,
                  tables=tables,
                  initializers=initializers,
                  mapdicts=mapdicts,
                  auto_commit=auto_commit)


def presenter(attribute=None):
    def custom_presenter(self, **keywords):
        keyword = _get_keyword_for_parameter(attribute)
        keywords[keyword] = attribute
        memory_source = factory.get_writable_source(**keywords)
        memory_source.write_data(self)
        return memory_source.content.getvalue()
    return custom_presenter


def importer(attribute=None):
    def custom_presenter1(self, content, **keywords):
        sheet_params = {}
        for field in constants.VALID_SHEET_PARAMETERS:
            if field in keywords:
                sheet_params[field] = keywords.pop(field)
        keyword = _get_keyword_for_parameter(attribute)
        if keyword == "file_type":
            keywords[keyword] = attribute
            keywords["file_content"] = content
        else:
            keywords[keyword] = content
        named_content = get_sheet_stream(**keywords)
        self.init(named_content.payload,
                  named_content.name, **sheet_params)

    return custom_presenter1


def book_presenter(attribute=None):
    def custom_presenter(self, **keywords):
        keyword = _get_keyword_for_parameter(attribute)
        keywords[keyword] = attribute
        memory_source = factory.get_writable_book_source(**keywords)
        memory_source.write_data(self)
        return memory_source.content.getvalue()
    return custom_presenter


def book_importer(attribute=None):
    def custom_book_importer(self, content, **keywords):
        keyword = _get_keyword_for_parameter(attribute)
        if keyword == "file_type":
            keywords[keyword] = attribute
            keywords["file_content"] = content
        else:
            keywords[keyword] = content
        sheets, filename, path = _get_book(**keywords)
        self.init(sheets=sheets, filename=filename, path=path)

    return custom_book_importer


def _get_book(**keywords):
    """Get an instance of :class:`Book` from an excel source

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    source = factory.get_book_source(**keywords)
    sheets = source.get_data()
    filename, path = source.get_source_info()
    return sheets, filename, path


def _try_put_file_read_pointer_to_its_begining(a_stream):
    if PY2:
        try:
            a_stream.seek(0)
        except IOError:
            pass
    else:
        import io
        try:
            a_stream.seek(0)
        except io.UnsupportedOperation:
            pass


def one_sheet_tuple(items):
    if not PY2:
        items = list(items)
    return items[0][0], items[0][1]


def _get_keyword_for_parameter(key):
    return factory.keywords.get(key, None)
