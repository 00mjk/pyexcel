"""
    pyexcel.plugin.parsers.sqlalchemy
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Export data into database datables

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel.parser import Parser
from pyexcel_io.constants import DB_SQL
import pyexcel_io.database.sql as sql
from pyexcel_io import get_data


# pylint: disable=W0223
class SQLAlchemyExporter(Parser):
    file_types = [DB_SQL]

    def parse_file_stream(self, file_stream,
                          export_columns_list=None, **keywords):
        session, tables = file_stream
        exporter = sql.SQLTableExporter(session)
        if export_columns_list is None:
            export_columns_list = [None] * len(tables)
        for table, export_columns in zip(tables, export_columns_list):
            adapter = sql.SQLTableExportAdapter(table, export_columns)
            exporter.append(adapter)
        sheets = get_data(exporter, streaming=True,
                          file_type=self._file_type, **keywords)
        return sheets
