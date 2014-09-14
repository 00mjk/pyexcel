"""
    pyexcel.readers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading different excel file formats

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from iterators import (HBRTLIterator,
                       HTLBRIterator,
                       VBRTLIterator,
                       VTLBRIterator,
                       RowIterator,
                       RowReverseIterator,
                       ColumnIterator,
                       ColumnReverseIterator,
                       SeriesColumnIterator)
from filters import (RowFilter,
                     ColumnIndexFilter)


class CSVReader:
    """
    csv reader
    """
    def __init__(self, file):
        import csv
        self.array = []
        reader = csv.reader(open(file, 'rb'), dialect=csv.excel)
        self.array.extend(reader)

    def number_of_sheets(self):
        """
        Number of sheets in the csv file
        """
        return 0

    def use_sheet_at_index(self, index):
        """Switch sheet for reading"""
        pass

    def use_sheet_named_as(self, name):
        """Switch sheet for reading"""        
        pass

    def sheet_names(self):
        """Get a list of sheet names"""        
        return ["csv"]

    def number_of_rows(self):
        """
        Number of rows in the csv file
        """
        return len(self.array)

    def number_of_columns(self):
        """
        Number of columns in the csv file

        assuming the length of each row is uniform
        """
        if len(self.array) > 1:
            return len(self.array[0])
        else:
            return 0

    def cell_value(self, row, column):
        """
        Random access to the csv cells
        """
        value = self.array[row][column]
        try:
            if "." in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            return value


class XLSReader:
    """
    xls reader

    Currently only support first sheet in the file
    """
    def __init__(self, file):
        import xlrd
        self.workbook = xlrd.open_workbook(file)
        self.worksheet = self.workbook.sheet_by_index(0)

    def number_of_sheets(self):
        """
        Number of sheets in the csv file
        """
        return self.workbook.nsheets

    def use_sheet_at_index(self, index):
        """Switch sheet for reading"""
        if index < self.workbook.nsheets:
            self.worksheet = self.workbook.sheet_by_index(0)

    def use_sheet_named_as(self, name):
        """Switch sheet for reading"""        
        self.worksheet = self.workbook.sheet_by_name(name)

    def sheet_names(self):
        """Get a list of sheet names"""        
        return self.workbook.sheet_names()

    def number_of_rows(self):
        """
        Number of rows in the xls file
        """
        return self.worksheet.nrows

    def number_of_columns(self):
        """
        Number of columns in the xls file
        """
        return self.worksheet.ncols

    def cell_value(self, row, column):
        """
        Random access to the xls cells
        """
        return self.worksheet.cell_value(row, column)


class ODSReaderImp(CSVReader):
    """
    ods reader

    Currently only support first sheet in the file
    """
    def __init__(self, file):
        import ext.odsreader as odsreader
        self.ods = odsreader.ODSReader(file)
        self.use_sheet_at_index(0)

    def number_of_sheets(self):
        """
        Number of sheets in the ods file
        """
        return len(self.ods.SHEETS.keys())

    def use_sheet_at_index(self, index):
        """Switch sheet for reading"""
        self.array = self.ods.getSheetByIndex(index)

    def use_sheet_named_as(self, name):
        """Switch sheet for reading"""        
        self.array =  self.ods.getSheet(name)

    def sheet_names(self):
        """Get a list of sheet names"""        
        return self.ods.sheetNames()


class Reader:
    """
    Wrapper class to unify csv, xls and xlsx reader
    """
    def __init__(self, file):
        """
        Reader constructor

        Selecting a specific reader according to file extension
        """
        if (file.endswith(".xlsm") or file.endswith(".xlsx") or file.endswith(".xls")):
            self.reader = XLSReader(file)
        elif file.endswith(".csv"):
            self.reader = CSVReader(file)
        elif file.endswith(".ods"):
            self.reader = ODSReaderImp(file)
        else:
            raise NotImplementedError("can not open %s" % file)
        self.current_sheet = 0

    def __iter__(self):
        """
        Default iterator to go through each cell one by one from top row to
        bottom row and from left to right
        """
        return self.enumerate()
        
    def enumerate(self):
        """
        Default iterator to go through each cell one by one from top row to
        bottom row and from left to right
        """
        return HTLBRIterator(self)

    def reverse(self):
        """
        Reverse iterator to go through each cell one by one from
        bottom row to top row and from right to left
        """
        return HBRTLIterator(self)

    def vertical(self):
        """
        Default iterator to go through each cell one by one from
        leftmost column to rightmost row and from top to bottom
        """
        return VTLBRIterator(self)

    def rvertical(self):
        """
        Default iterator to go through each cell one by one from rightmost
        column to leftmost row and from bottom to top
        """
        return VBRTLIterator(self)

    def rows(self):
        """
        Returns a row iterator to go through each row from top to bottom
        """
        return RowIterator(self)

    def rrows(self):
        """
        Returns a row iterator to go through each row from bottom to top
        """
        return RowReverseIterator(self)

    def columns(self):
        """
        Returns a column iterator to go through each column from left to right
        """
        return ColumnIterator(self)

    def rcolumns(self):
        """
        Returns a column iterator to go through each column from right to left
        """
        return ColumnReverseIterator(self)

    def number_of_rows(self):
        """
        Number of rows in the data file
        """
        return self.reader.number_of_rows()

    def number_of_columns(self):
        """
        Number of columns in the data file
        """
        return self.reader.number_of_columns()

    def cell_value(self, row, column):
        """
        Random access to the data cells
        """
        if row in self.row_range() and column in self.column_range():
            return self.reader.cell_value(row, column)
        else:
            return None

    def row_range(self):
        """
        Utility function to get row range
        """
        return range(0, self.reader.number_of_rows())

    def column_range(self):
        """
        Utility function to get column range
        """
        return range(0, self.reader.number_of_columns())

    def row_at(self, index):
        """
        Returns an array that collects all data at the specified row
        """
        if index in self.row_range():
            cell_array = []
            for i in self.column_range():
                cell_array.append(self.cell_value(index, i))
            return cell_array
        else:
            return None

    def column_at(self, index):
        """
        Returns an array that collects all data at the specified column
        """
        if index in self.column_range():
            cell_array = []
            for i in self.row_range():
                cell_array.append(self.cell_value(i, index))
            return cell_array
        else:
            return None

    def contains(self, predicate):
        for r in self.rows():
            if predicate(r):
                return True
        else:
            return False

    def number_of_sheets(self):
        """
        Number of sheets in the ods file
        """
        return self.reader.number_of_sheets()

    def use_sheet_at_index(self, index):
        """Switch sheet for reading"""
        self.reader.use_sheet_at_index(index)
        self.current_sheet = index
        
    def use_sheet_named_as(self, name):
        """Switch sheet for reading"""        
        self.reader.use_sheet_named_as(name)
        names = self.sheet_names()
        index = names.index(name)
        self.current_sheet = index

    def sheet_names(self):
        """Get a list of sheet names"""        
        return self.reader.sheet_names()

    def sheet(self):
        """Get current sheet index"""
        return self.current_sheet

class FilterableReader(Reader):
    """
    Reader that can be applied one filter
    """
    
    _filter = None

    def row_range(self):
        if self._filter:
            new_rows = self.reader.number_of_rows() - self._filter.rows()
            return range(0, new_rows)
        else:
            return range(0, self.reader.number_of_rows())

    def column_range(self):
        if self._filter:
            new_cols = self.reader.number_of_columns() - self._filter.columns()
            return range(0, new_cols)
        else:
            return range(0, self.reader.number_of_columns())

    def number_of_rows(self):
        """
        Number of rows in the data file
        """
        if self._filter:
            return self.reader.number_of_rows() - self._filter.rows()
        else:
            return self.reader.number_of_rows()

    def number_of_columns(self):
        """
        Number of columns in the data file
        """
        if self._filter:
            return self.reader.number_of_columns() - self._filter.columns()
        else:
            return self.reader.number_of_columns()

    def cell_value(self, row, column):
        """
        Random access to the data cells
        """
        if row in self.row_range() and column in self.column_range():
            if self._filter:
                new_row, new_column = self._filter.translate(row, column)
                return self.reader.cell_value(new_row, new_column)
            else:
                return self.reader.cell_value(row, column)
        else:
            return None

    def filter(self, afilter):
        afilter.validate_filter(self)
        self._filter = afilter
        return self


class GenericSeriesReader(FilterableReader):
    """
    For data with column headers

    x y z
    1 2 3
    4 5 6

    This class has a default filter that filter out
    row 0 as headers. Extra functions were added
    to return headers at row 0
    """
    def __init__(self, reader):
        self.reader = reader
        # filter out the first row
        self.filter(RowFilter([0]))
        self.headers = None

    def _headers(self):
        self.headers = []
        for i in self.column_range():
            self.headers.append(self.reader.cell_value(0, i))

    def series(self):
        self._headers()
        return self.headers

    def named_column_at(self, name):
        self._headers()
        index = self.headers.index(name)
        column_array = self.column_at(index)
        return {name: column_array}

    def __iter__(self):
        return SeriesColumnIterator(self)


class StaticSeriesReader(GenericSeriesReader):
    """

    Static Series Reader. No filters can be applied.
    """
    def __init__(self, file):
        reader = Reader(file)
        GenericSeriesReader.__init__(self, reader)


class ColumnFilterableSeriesReader(GenericSeriesReader):
    """

    Columns can be filtered but not rows
    """
    def __init__(self, file):
        self.reader = FilterableReader(file)
        GenericSeriesReader.filter(self, RowFilter([0]))
        self.headers = None

    def filter(self, filter):
        self.reader.filter(filter)
        self._filter.validate_filter(self)


class SeriesReader(GenericSeriesReader):
    """

    rows other than header row can be filtered. row number
    has been shifted by 1 as header row is protected.

    columns can be filtered.
    """
    def __init__(self, file):
        self.reader = ColumnFilterableSeriesReader(file)

    def series(self):
        return self.reader.series()

    def named_column_at(self, name):
        headers = self.series()
        index = headers.index(name)
        column_array = self.column_at(index)
        return {name: column_array}

    def filter(self, afilter):
        if isinstance(afilter, ColumnIndexFilter):
            self.reader.filter(afilter)
        else:
            GenericSeriesReader.filter(self, afilter)
