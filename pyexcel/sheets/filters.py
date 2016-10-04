"""
    pyexcel.filters
    ~~~~~~~~~~~~~~~

    Filtering functions for pyexcel readers

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details

"""
from pyexcel._compact import PY2


class IndexFilter(object):
    """A generic index filter"""
    def __init__(self, func):
        """Constructor
        :param Function func: a evaluation function
        """
        self.eval_func = func
        self.shallow_eval_func = None
        # indices to be filtered out
        self.indices = None

    def invert(self):
        if self.eval_func:
            if self.shallow_eval_func is None:
                self.shallow_eval_func = self.eval_func

                def inverse(val): return not self.shallow_eval_func(val)
                self.eval_func = inverse
            else:
                self.eval_func = self.shallow_eval_func
                self.shallow_eval_func = None
        return self

    def rows(self):
        """Rows that were filtered out
        """
        return 0

    def columns(self):
        """Columns that were filtered out"""
        return 0

    def validate_filter(self, reader):
        """
        Find out which column index to be filtered

        :param Matrix reader: a Matrix instance

        """
        pass


class RegionFilter(IndexFilter):
    """Filter on both row index and column index"""

    def __init__(self, row_slice, column_slice):
        """Constructor

        :param slice row_slice: row index range
        :param slice column_slice: column index range
        """
        self.row_indices = range(row_slice.start,
                                 row_slice.stop,
                                 row_slice.step)
        self.column_indices = range(column_slice.start,
                                    column_slice.stop,
                                    column_slice.step)
        if not PY2:
            self.row_indices = list(self.row_indices)
            self.column_indices = list(self.column_indices)

    def columns(self):
        """Columns that were filtered out"""
        return len(self.column_indices)

    def rows(self):
        """Rows that were filtered out"""
        return len(self.row_indices)

    def validate_filter(self, reader):
        self.row_indices = [i for i in reader.row_range()
                            if i not in self.row_indices]
        self.column_indices = [i for i in reader.column_range()
                               if i not in self.column_indices]


class ColumnIndexFilter(IndexFilter):
    """A column filter that operates on column indices"""
    def columns(self):
        """Columns that were filtered out"""
        return len(self.indices)

    def validate_filter(self, reader):
        """
        Find out which column index to be filtered

        :param Matrix reader: a Matrix instance
        """
        self.indices = [i for i in reader.column_range() if self.eval_func(i)]


class ColumnFilter(ColumnIndexFilter):
    """Filters out a list of columns"""
    def __init__(self, indices):
        """Constructor

        :param list indices: a list of column indices to be filtered out
        """
        def eval_func(x): return x in indices
        ColumnIndexFilter.__init__(self, eval_func)


class SingleColumnFilter(ColumnIndexFilter):
    """Filters out a single column index"""
    def __init__(self, index):
        """Constructor

        :param list indices: a list of column indices to be filtered out
        """
        def eval_func(x): return x == index
        ColumnIndexFilter.__init__(self, eval_func)


class OddColumnFilter(ColumnIndexFilter):
    """Filters out odd indexed columns

    * column 0 is regarded as the first column.
    * column 1 is regarded as the second column -> this will be filtered out
    """
    def __init__(self):
        def eval_func(x): return (x+1) % 2 == 1
        ColumnIndexFilter.__init__(self, eval_func)


class EvenColumnFilter(ColumnIndexFilter):
    """Filters out even indexed columns

    * column 0 is regarded as the first column. -> this will be filtered out
    * column 1 is regarded as the second column
    """
    def __init__(self):
        def eval_func(x): return (x+1) % 2 == 0
        ColumnIndexFilter.__init__(self, eval_func)


class RowIndexFilter(IndexFilter):
    """Filter out rows by its row index """
    def rows(self):
        """number of rows to be filtered out"""
        if self.indices:
            return len(self.indices)
        else:
            return 0

    def validate_filter(self, reader):
        """
        Find out which column index to be filtered

        :param Matrix reader: a Matrix instance
        """
        self.indices = [i for i in reader.row_range() if self.eval_func(i)]


class RowFilter(RowIndexFilter):
    """Filters a list of rows"""
    def __init__(self, indices):
        """Constructor

        :param list indices: a list of column indices to be filtered out
        """
        def eval_func(x): return x in indices
        RowIndexFilter.__init__(self, eval_func)


class SingleRowFilter(RowIndexFilter):
    """Filters out a single row"""
    def __init__(self, index):
        """Constructor

        :param list indices: a list of column indices to be filtered out
        """
        def eval_func(x): return x == index
        RowIndexFilter.__init__(self, eval_func)


class OddRowFilter(RowIndexFilter):
    """Filters out odd indexed rows

    row 0 is seen as the first row
    """
    def __init__(self):
        def eval_func(x): return (x+1) % 2 == 1
        RowIndexFilter.__init__(self, eval_func)


class EvenRowFilter(RowIndexFilter):
    """Filters out even indexed rows

    row 0 is seen as the first row
    """
    def __init__(self):
        def eval_func(x): return (x+1) % 2 == 0
        RowIndexFilter.__init__(self, eval_func)


class RowValueFilter(RowIndexFilter):
    """Filters out rows based on its row values

    .. note:: it takes time as it needs to go through all values
    """
    def validate_filter(self, reader):
        """
        Filter out the row indices

        This is what it does::

            new_indices = []
            index = 0
            for r in reader.rows():
                if not self.eval_func(r):
                    new_indices.append(index)
                index += 1

        :param Matrix reader: a Matrix instance
        """
        self.indices = [row[0]
                        for row in enumerate(reader.rows())
                        if self.eval_func(row[1])]


class NamedRowValueFilter(RowIndexFilter):
    """Filter out rows that satisfy a condition

    .. note:: it takes time as it needs to go through all values
    """
    def validate_filter(self, reader):
        """
        Filter out the row indices

        This is what it does::

            new_indices = []
            index = 0
            for r in reader.rows():
                if not self.eval_func(r):
                    new_indices.append(index)
                index += 1

        :param Matrix reader: a Matrix instance
        """
        series = reader.colnames
        self.indices = [row[0]
                        for row in enumerate(reader.rows())
                        if self.eval_func(dict(zip(series, row[1])))]


class SeriesRowValueFilter(NamedRowValueFilter):
    """Backword compactibility"""
    pass


class ColumnValueFilter(ColumnIndexFilter):
    """Filters out rows based on its row values

    .. note:: it takes time as it needs to go through all values
    """
    def validate_filter(self, reader):
        """
        Filter out the row indices

        This is what it does::

            new_indices = []
            index = 0
            for r in reader.rows():
                if not self.eval_func(r):
                    new_indices.append(index)
                index += 1

        :param Matrix reader: a Matrix instance
        """
        self.indices = [column[0]
                        for column in enumerate(reader.columns())
                        if self.eval_func(column[1])]


class NamedColumnValueFilter(ColumnIndexFilter):
    """Filter out rows that satisfy a condition

    .. note:: it takes time as it needs to go through all values
    """
    def validate_filter(self, reader):
        """
        Filter out the row indices

        This is what it does::

            new_indices = []
            index = 0
            for r in reader.rows():
                if not self.eval_func(r):
                    new_indices.append(index)
                index += 1

        :param Matrix reader: a Matrix instance
        """
        series = reader.rownames
        self.indices = [column[0]
                        for column in enumerate(reader.columns())
                        if self.eval_func(dict(zip(series, column[1])))]


class RowInFileFilter(RowValueFilter):
    """Filter out rows that has a row from another reader"""
    def __init__(self, reader):
        """
        Constructor

        :param Matrix reader: a Matrix instance
        """
        def func(row_a):
            def are_we_equal(row_b): return row_a == row_b
            return not reader.contains(are_we_equal)

        RowValueFilter.__init__(self, func)
