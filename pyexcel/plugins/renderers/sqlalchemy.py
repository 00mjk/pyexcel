from pyexcel.renderer import Renderer
from pyexcel_io import save_data
from pyexcel_io.constants import DB_SQL
from pyexcel._compact import OrderedDict
import pyexcel_io.database.sql as sql
from pyexcel.internal.generators import BookStream


NO_COLUMN_NAMES = "Only sheet with column names is accepted"


class SQLAlchemyRenderer(Renderer):
    file_types = [DB_SQL]

    def get_io(self):
        raise Exception("No io for this renderer")

    def render_sheet_to_file(self, file_name, sheet, **keywords):
        raise NotImplementedError("We are not writing to file")

    def render_book_to_file(self, file_name, book, **keywords):
        raise NotImplementedError("We are not writing to file")

    def render_sheet_to_stream(self, file_stream, sheet,
                               init=None, mapdict=None, **keywords):
        headers = sheet.colnames
        if len(headers) == 0:
            raise Exception(NO_COLUMN_NAMES)
        importer = sql.SQLTableImporter(file_stream[0])
        adapter = sql.SQLTableImportAdapter(file_stream[1])
        adapter.column_names = headers
        adapter.row_initializer = init
        adapter.column_name_mapping_dict = mapdict
        importer.append(adapter)
        save_data(importer, {adapter.get_name(): sheet.get_internal_array()},
                  file_type=self._file_type, **keywords)

    def render_book_to_stream(self, file_stream, book,
                              inits=None, mapdicts=None, **keywords):
        from pyexcel.book import to_book
        session, tables = file_stream
        thebook = book
        if isinstance(book, BookStream):
            thebook = to_book(book)
        initializers = inits
        if initializers is None:
            initializers = [None] * len(tables)
        if mapdicts is None:
            mapdicts = [None] * len(tables)
        for sheet in thebook:
            if len(sheet.colnames) == 0:
                sheet.name_columns_by_row(0)
        colnames_array = [sheet.colnames for sheet in book]
        scattered = zip(tables, colnames_array, mapdicts, initializers)

        importer = sql.SQLTableImporter(session)
        for each_table in scattered:
            adapter = sql.SQLTableImportAdapter(each_table[0])
            adapter.column_names = each_table[1]
            adapter.column_name_mapping_dict = each_table[2]
            adapter.row_initializer = each_table[3]
            importer.append(adapter)
        to_store = OrderedDict()
        for sheet_name in thebook.sheet_names():
            # due book.to_dict() brings in column_names
            # which corrupts the data
            to_store[sheet_name] = book[sheet_name].get_internal_array()
        save_data(importer, to_store, file_type=self._file_type, **keywords)
