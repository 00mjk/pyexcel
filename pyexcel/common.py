import xlrd
import copy
from iterators import (HBRTLIterator,
                       HTLBRIterator,
                       VBRTLIterator,
                       VTLBRIterator,
                       RowIterator,
                       RowReverseIterator,
                       ColumnIterator,
                       ColumnReverseIterator,
                       SeriesColumnIterator)
from filters import (RowIndexFilter,
                     ColumnIndexFilter,
                     RowFilter)
import datetime


DATE_FORMAT = "d"
FLOAT_FORMAT = "f"
INT_FORMAT = "i"
UNICODE_FORMAT = "u"
STRING_FORMAT = "s"
BOOLEAN_FORMAT = "b"
EMPTY = "e"


XLS_FORMAT_CONVERSION = {
    xlrd.XL_CELL_TEXT: STRING_FORMAT,
    xlrd.XL_CELL_EMPTY: EMPTY,
    xlrd.XL_CELL_DATE: DATE_FORMAT,
    xlrd.XL_CELL_NUMBER: FLOAT_FORMAT,
    xlrd.XL_CELL_BOOLEAN: INT_FORMAT,
    xlrd.XL_CELL_BLANK: EMPTY,
    xlrd.XL_CELL_ERROR: EMPTY
}


PYTHON_TYPE_CONVERSION = {
    float: FLOAT_FORMAT,
    int: INT_FORMAT,
    datetime.date: DATE_FORMAT,
    datetime.time: DATE_FORMAT,
    datetime.datetime: DATE_FORMAT,
    str: STRING_FORMAT,
    bool: BOOLEAN_FORMAT
}


def f7(seq):
    """
    Reference:
    http://stackoverflow.com/questions/480214/
    how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
    """
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]


class RawSheet:
    """
    xls sheet

    Currently only support first sheet in the file
    """
    def __init__(self, array):
        self.array = array
        self._formatters = []

    def add_formatter(self, aformatter):
        self._formatters.append(aformatter)

    def remove_formatter(self, aformatter):
        self._formatters.remove(aformatter)

    def clear_formatters(self):
        self._formatters = []

    def number_of_rows(self):
        """
        Number of rows in the xls sheet
        """
        return len(self.array)

    def number_of_columns(self):
        """
        Number of columns in the xls sheet
        """
        if self.number_of_rows() > 0:
            return len(self.array[0])
        else:
            return 0

    def extend_rows(self, rows):
        """expected the rows to be off the same length"""
        array_length = self.number_of_columns()
        for r in rows:
            length = len(r)
            agreed_length = min (length, array_length)
            array = copy.deepcopy(r[:agreed_length])
            if length < array_length:
                array = array + [""] * (array_length-length)
            self.array.append(array)

    def delete_rows(self, row_indices):
        """delete rows"""
        if isinstance(row_indices, list) is False:
            raise ValueError
        if len(row_indices) > 0:
            unique_list = f7(row_indices)
            sorted_list = sorted(unique_list, reverse=True)
            for i in sorted_list:
                if i < self.number_of_rows():
                    del self.array[i]
        
    def cell_value(self, row, column, new_value=None):
        """
        Random access to the xls cells
        """
        if new_value == None:
            value = self.array[row][column]
            value_type = PYTHON_TYPE_CONVERSION.get(type(value),
                                              STRING_FORMAT)
            if len(self._formatters) > 0:
                previous_type = value_type
                for f in self._formatters:
                    if f.is_my_business(row, column, value):
                        value = f.do_format(value, previous_type)
                        previous_type = f.desired_format
            else:
                if value_type == STRING_FORMAT:
                    try:
                        if "." in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass
            return value
        else:
            self.array[row][column] = new_value
            return new_value


class PlainSheet:
    """
    Wrapper class to unify csv, xls and xlsx sheet
    """
    def __init__(self, sheet):
        """
        Sheet constructor

        Selecting a specific sheet according to file extension
        """
        self.sheet = sheet

    def __iter__(self):
        """
        Default iterator to go through each cell one by one from top row to
        bottom row and from left to right
        """
        return self.rows()

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
        Number of rows in the data sheet
        """
        return self.sheet.number_of_rows()

    def number_of_columns(self):
        """
        Number of columns in the data sheet
        """
        return self.sheet.number_of_columns()

    def cell_value(self, row, column, new_value=None):
        """
        Random access to the data cells
        """
        if row in self.row_range() and column in self.column_range():
            # apply formatting
            return self.sheet.cell_value(row, column, new_value)
        else:
            return None

    def row_range(self):
        """
        Utility function to get row range
        """
        return range(0, self.sheet.number_of_rows())

    def column_range(self):
        """
        Utility function to get column range
        """
        return range(0, self.sheet.number_of_columns())

    def __setitem__(self, aslice, c):
        if isinstance(aslice, slice):
            start = max(aslice.start, 0)
            stop = min(aslice.stop, self.number_of_rows())
            if start > stop:
                raise ValueError
            elif start < stop:
                if aslice.step:
                    my_range = range(start, stop, aslice.step)
                else:
                    my_range = range(start, stop)
                for i in my_range:
                    self.set_row_at(i, c)
            else:
                # start == stop
                self.set_row_at(start, c)
        else:
            self.set_row_at(aslice, c)

    def __getitem__(self, aslice):
        """By default, this class recognize from top to bottom
        from left to right"""
        index = aslice
        if isinstance(aslice, slice):
            start = max(aslice.start, 0)
            stop = min(aslice.stop, self.number_of_rows())
            if start > stop:
                return None
            elif start < stop:
                if aslice.step:
                    my_range = range(start, stop, aslice.step)
                else:
                    my_range = range(start, stop)
                results = []
                for i in my_range:
                    results.append(self.row_at(i))
                return results
            else:
                # drop this to index handler
                index = start
        if index in self.row_range():
            return self.row_at(index)
        else:
            raise IndexError

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

    def set_column_at(self, column_index, data_array, starting=0):
        if column_index < self.number_of_columns() and starting < self.number_of_rows():
            to = min(len(data_array)+starting, self.number_of_rows())
            for i in range(starting, to):
                self.cell_value(i, column_index, data_array[i])
        else:
            raise ValueError

    def set_row_at(self, row_index, data_array, starting=0):
        if row_index < self.number_of_rows() and starting < self.number_of_columns():
            to = min(len(data_array)+starting, self.number_of_columns())
            for i in range(starting, to):
                self.cell_value(row_index,i, data_array[i])
        else:
            raise ValueError

    def contains(self, predicate):
        for r in self.rows():
            if predicate(r):
                return True
        else:
            return False

    def add_formatter(self, aformatter):
        self.sheet.add_formatter(aformatter)

    def remove_formatter(self, aformatter):
        self.sheet.remove_formatter(aformatter)

    def clear_formatters(self):
        self.sheet.clear_formatters()

    def extend_rows(self, rows):
        """expected the rows to be off the same length"""
        self.sheet.extend_rows(rows)

    def delete_rows(self, row_indices):
        """delete rows"""
        self.sheet.delete_rows(row_indices)


class MultipleFilterableSheet(PlainSheet):
    """
    Sheet that can be applied one filter
    """
    def __init__(self, sheet):
        PlainSheet.__init__(self, sheet)
        self._filters = []

    def row_range(self):
        """
        row range
        """
        return range(0, self.number_of_rows())

    def column_range(self):
        """
        column range
        """
        return range(0, self.number_of_columns())

    def number_of_rows(self):
        """
        Number of rows in the data sheet
        """
        if len(self._filters) != 0:
            new_rows = self.sheet.number_of_rows()
            for filter in self._filters:
                new_rows = new_rows - filter.rows()
            return new_rows
        else:
            return self.sheet.number_of_rows()

    def number_of_columns(self):
        """
        Number of columns in the data sheet
        """
        if len(self._filters) != 0:
            new_cols = self.sheet.number_of_columns()
            for filter in self._filters:
                new_cols = new_cols - filter.columns()
            return new_cols
        else:
            return self.sheet.number_of_columns()

    def cell_value(self, row, column, new_value=None):
        """
        Random access to the data cells
        """
        if row in self.row_range() and column in self.column_range():
            if len(self._filters) != 0:
                new_row = row
                new_column = column
                number_of_filters = len(self._filters)
                for i in range(number_of_filters-1, -1, -1):
                    new_row, new_column = self._filters[i].translate(
                        new_row,
                        new_column)
                return self.sheet.cell_value(new_row, new_column, new_value)
            else:
                return self.sheet.cell_value(row, column, new_value)
        else:
            return None

    def add_filter(self, afilter):
        """Apply a filter"""
        afilter.validate_filter(self)
        self._filters.append(afilter)
        return self

    def remove_filter(self, afilter):
        """Remove a named filter

        have to remove all filters in order to re-validate the
        rest of the filters
        """
        self._filters.remove(afilter)
        local_filters = self._filters
        self._filters = []
        for f in local_filters:
            f.validate_filter(self)
            self._filters.append(f)

    def clear_filters(self):
        """Clears all filters"""
        self._filters = []

    def filter(self, afilter):
        """This is short hand for add_filter"""
        self.add_filter(afilter)

    def extend_rows(self, rows):
        """expected the rows to be off the same length

        too expensive to do so
        """
        raise NotImplementedError

    def delete_rows(self, row_indices):
        """delete rows

        too expensive to do so
        """
        raise NotImplementedError


class Sheet(MultipleFilterableSheet):
    def __init__(self, sheet, name):
        MultipleFilterableSheet.__init__(self, sheet)
        self.column_filters = []
        self.row_filters = []
        self.headers = None
        self.signature_filter = None
        self.name = name

    def become_series(self):
        """
        Evolve this sheet to a SeriesReader
        """
        self.signature_filter = RowFilter([0])
        self._validate_filters()
        return self

    def become_sheet(self):
        """
        Evolve back to plain sheet reader
        """
        self.signature_filter = None
        self._validate_filters()
        return self

    def add_filter(self, afilter):
        """
        Apply a filter
        """
        if isinstance(afilter, ColumnIndexFilter):
            self.column_filters.append(afilter)
        elif isinstance(afilter, RowIndexFilter):
            self.row_filters.append(afilter)
        self._validate_filters()

    def clear_filters(self):
        """
        Clear all filters
        """
        self.column_filters = []
        self.row_filters = []
        self._validate_filters()

    def remove_filter(self, afilter):
        """
        Remove a named custom filter
        """
        if isinstance(afilter, ColumnIndexFilter):
            self.column_filters.remove(afilter)
        elif isinstance(afilter, RowIndexFilter):
            self.row_filters.remove(afilter)
        self._validate_filters()

    def _validate_filters(self):
        if self.signature_filter:
            local_filters = (self.column_filters +
                             [self.signature_filter] +
                             self.row_filters)
        else:
            local_filters = self.column_filters + self.row_filters
        self._filters = []
        for filter in local_filters:
            filter.validate_filter(self)
            self._filters.append(filter)

    def _headers(self):
        self.headers = []
        for i in self.column_range():
            new_row = 0
            new_column = i
            number_of_column_filters = len(self.column_filters)
            for x in range(number_of_column_filters-1, -1, -1):
                new_row, new_column = self.column_filters[x].translate(
                    new_row,
                    new_column)
            self.headers.append(self.sheet.cell_value(0, new_column))

    def series(self):
        """
        Return column headers
        """
        if self.signature_filter:
            self._headers()
            return self.headers
        else:
            return []

    def named_column_at(self, name):
        """Get a column by its name """
        if self.signature_filter:
            self._headers()
            index = self.headers.index(name)
            column_array = self.column_at(index)
            return {name: column_array}
        else:
            return {}

    def __iter__(self):
        if self.signature_filter:
            return SeriesColumnIterator(self)
        else:
            return MultipleFilterableSheet.__iter__(self)
