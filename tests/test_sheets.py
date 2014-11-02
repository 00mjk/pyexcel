import pyexcel as pe
from _compact import OrderedDict

    
class TestPlainSheet:
    def setUp(self):
        self.data = [
            [1, 2, 3, 4, 5, 6, 7, 8],
            ["1", "2", "3", "4", "5", "6", "7", "8"],
            [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7,7", "8.8"],
            [2, 3, 4, 5, 6, 7, 8, 9],
            ["2", "3", "4", "5", "6", "7", "8", "9"]            
        ]

    def test_apply_row_formatter(self):
        s = pe.sheets.PlainSheet(self.data)
        s.apply_formatter(pe.formatters.RowFormatter(0, str))
        assert s.row[0] == s.row[1]

    def test_apply_column_formatter(self):
        s = pe.sheets.PlainSheet(self.data)
        s.apply_formatter(pe.formatters.ColumnFormatter(0, float))
        assert s.column[0] == [1, 1, 1.1, 1.1, 2, 2]

    def test_apply_sheet_formatter(self):
        s = pe.sheets.PlainSheet(self.data)
        s.format(pe.formatters.SheetFormatter(float))
        assert s.row[0] == s.row[1]
        assert s.column[0] == [1, 1, 1.1, 1.1, 2, 2]

    def test_freeze_formatter(self):
        s = pe.sheets.PlainSheet(self.data)
        s.freeze_formatters()

    def test_empty_sheet(self):
        s = pe.sheets.PlainSheet([])
        ret = s.cell_value(100, 100)
        assert ret is None
        ret = s._cell_value(100, 100)
        assert ret == ""
        
class TestFilterSheet:
    def test_freeze_filters(self):
        data = [
            [1, 2, 3],
            [2, 3, 4]
        ]
        s = pe.sheets.MultipleFilterableSheet(data)
        s.add_filter(pe.filters.EvenRowFilter())
        s.freeze_filters()
        assert s.row[0] == [1, 2, 3]
        assert s.column[0] == [1]

    def test_non_filter(self):
        data = []
        s = pe.sheets.MultipleFilterableSheet(data)
        try:
            s.filter("abc")
            assert 1==2
        except NotImplementedError:
            assert 1==1


class TestSheetNamedColumn:
    def setUp(self):
        self.data = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]

    def test_formatter_by_named_column(self):
        """Test one named column"""
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_row(0)
        f = pe.formatters.NamedColumnFormatter("Column 1", str)
        s.format(f)
        assert s.column["Column 1"] == ["1", "4", "7"]
        
    def test_formatter_by_named_columns(self):
        """Test multiple named columns"""
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_row(0)
        f = pe.formatters.NamedColumnFormatter(["Column 1", "Column 3"], str)
        s.format(f)
        assert s.column["Column 1"] == ["1", "4", "7"]
        assert s.column["Column 3"] == ["3", "6", "9"]

    def test_formatter_by_named_column3(self):
        """Test multiple named columns with wrong type"""
        try:
            pe.formatters.NamedColumnFormatter(["Column 1", 1], str)
            assert 1==2
        except IndexError:
            assert 1==1
        try:
            pe.formatters.NamedColumnFormatter([], str)
            assert 1==2
        except IndexError:
            assert 1==1
        try:
            pe.formatters.NamedColumnFormatter(1.22, str)
            assert 1==2
        except NotImplementedError:
            assert 1==1
        
    def test_add(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_row(0)
        data = OrderedDict({
            "Column 4":[10, 11,12]
        })
        s = s.column + data
        assert s.column["Column 4"] == [10, 11, 12]

    def test_add_wrong_type(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_row(0)
        try:
            s = s.column + "string type"
            assert 1==2
        except TypeError:
            assert 1==1

    def test_delete_named_column(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_row(0)
        del s.column["Column 2"]
        assert s.number_of_columns() == 2
        print(s.row_series)
        try:
            s.column["Column 2"]
            assert 1==2
        except ValueError:
            assert 1==1
            
    def test_delete_indexed_column(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_row(0)
        del s.column[1]
        assert s.number_of_columns() == 2
        try:
            s.column["Column 2"]
            assert 1==2
        except ValueError:
            assert 1==1


class TestSheetNamedColumn2:
    def setUp(self):
        self.data = [
            [1, 2, 3],
            [4, 5, 6],
            ["Column 1", "Column 2", "Column 3"],
            [7, 8, 9]
        ]

    def test_series(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_row(2)
        assert s.row_series == ["Column 1", "Column 2", "Column 3"]

    def test_formatter_by_named_column(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_row(2)
        f = pe.formatters.NamedColumnFormatter("Column 1", str)
        s.format(f)
        assert s.column["Column 1"] == ["1", "4", "7"]

    def test_add(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_row(2)
        data = OrderedDict({
            "Column 4": [10, 11, 12]
            }
        )
        s = s.column + data
        assert s.column["Column 4"] == [10, 11, 12]

    def test_delete_named_column(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_row(2)
        del s.column["Column 2"]
        assert s.number_of_columns() == 2
        try:
            s.column["Column 2"]
            assert 1==2
        except ValueError:
            assert 1==1

    def test_set_indexed_row(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_row(2)
        s.row[0] = [10000, 1, 11]
        assert s.row[0] == [10000, 1, 11]

    def test_add_an_array(self):
        """Before IndexSheet become a series sheet, it should
        add array"""


class TestSheetNamedRow:
    def setUp(self):
        self.data = [
            ["Row 0", -1, -2, -3],
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9]
        ]

    def test_formatter_by_named_row(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_column(0)
        f = pe.formatters.NamedRowFormatter("Row 1", str)
        s.format(f)
        assert s.row["Row 1"] == ["1", "2", "3"]

    def test_formatter_by_named_row2(self):
        """Test a list of string as index"""
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_column(0)
        f = pe.formatters.NamedRowFormatter(["Row 1", "Row 2"], str)
        s.format(f)
        assert s.row["Row 1"] == ["1", "2", "3"]
        assert s.row["Row 2"] == ["4", "5", "6"]

    def test_formatter_by_named_column3(self):
        """Test multiple named columns with wrong type"""
        try:
            pe.formatters.NamedRowFormatter(["Row 1", 1], str)
            assert 1==2
        except IndexError:
            assert 1==1
        try:
            pe.formatters.NamedRowFormatter([], str)
            assert 1==2
        except IndexError:
            assert 1==1
        try:
            pe.formatters.NamedRowFormatter(1.22, str)
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def test_add(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_column(0)
        data = OrderedDict({
            "Row 5": [10, 11, 12]
            }
        )
        s = s.row + data
        assert s.row["Row 5"] == [10, 11, 12]

    def test_add_wrong_type(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_column(0)
        try:
            s = s.row + "string type"
            assert 1==2
        except TypeError:
            assert 1==1

    def test_delete_named_column(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_column(0)
        del s.row["Row 2"]
        assert s.number_of_rows() == 3
        try:
            s.row["Row 2"]
            assert 1==2
        except ValueError:
            assert 1==1
            
    def test_delete_indexed_column(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_column(0)
        del s.row[2]
        assert s.number_of_rows() == 3
        try:
            s.row["Row 2"]
            assert 1==2
        except ValueError:
            assert 1==1

    def test_set_named_row(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_column(0)
        s.row["Row 2"] = [11, 11, 11]
        assert s.row["Row 2"] == [11, 11, 11]

    def test_set_indexed_column(self):
        s = pe.sheets.IndexSheet(self.data, "test")
        s.index_by_column(0)
        s.column[0] = [12,3,4,5]
        assert s.column[0] == [12, 3, 4, 5]
