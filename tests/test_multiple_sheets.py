from base import PyexcelMultipleSheetBase
import pyexcel as pe
import os
from base import create_sample_file1
import sys
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict


class TestXlsNXlsmMultipleSheets(PyexcelMultipleSheetBase):
    def setUp(self):
        self.testfile = "multiple1.xls"
        self.testfile2 = "multiple1.xlsm"
        self.content = OrderedDict()
        self.content.update({"Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]})
        self.content.update({"Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]})
        self.content.update({"Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]})
        self._write_test_file(self.testfile)

    def tearDown(self):
        self._clean_up()

class TestSingleSheetReaderForMulitpleSheetBook:
    def setUp(self):
        self.testfile = "multiple1.xls"
        self.content = OrderedDict()
        self.content.update({"Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]})
        self.content.update({"Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]})
        self.content.update({"Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]})
        w = pe.BookWriter(self.testfile)
        w.write_book_from_dict(self.content)
        w.close()

    def test_non_default_sheet_as_single_sheet_reader(self):
        r = pe.Reader(self.testfile, "Sheet1")
        data = pe.utils.to_array(r)
        assert data == self.content["Sheet1"]
        r2 = pe.Reader(self.testfile, "Sheet2")
        data = pe.utils.to_array(r2)
        assert data == self.content["Sheet2"]
        r3 = pe.Reader(self.testfile, "Sheet3")
        data = pe.utils.to_array(r3)
        assert data == self.content["Sheet3"]

    def test_non_default_sheet_as_single_sheet_reader_series(self):
        r = pe.SeriesReader(self.testfile, "Sheet3")
        data = pe.utils.to_array(r.rows())
        assert data == self.content["Sheet3"][1:]

    def test_non_default_sheet_as_single_sheet_plain_reader(self):
        r = pe.PlainReader(self.testfile, "Sheet2")
        data = pe.utils.to_array(r.rows())
        assert data == self.content["Sheet2"]

    def test_non_default_sheet_as_single_sheet_filterable_reader(self):
        r = pe.FilterableReader(self.testfile, "Sheet2")
        data = pe.utils.to_array(r.rows())
        assert data == self.content["Sheet2"]

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestReader:
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,1.1,1
        """
        self.testfile = "testcsv.csv"
        self.rows = 3
        create_sample_file1(self.testfile)

    def test_csv_book_reader(self):
        r = pe.BookReader(self.testfile)
        assert r.number_of_sheets() == 1
        assert r.sheet_names() == ["csv"]

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)

class TestAddBooks:
    def _write_test_file(self, file, content):
        """
        Make a test file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        w = pe.BookWriter(file)
        w.write_book_from_dict(content)
        w.close()

    def setUp(self):
        self.testfile = "multiple1.xlsm"
        self.testfile2 = "multiple1.xls"
        self.testfile3 = "multiple2.xlsx"
        self.content = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
        self._write_test_file(self.testfile, self.content)
        self._write_test_file(self.testfile2, self.content)
        self.test_single_sheet_file = "single.xls"
        self.content1 = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
        }
        self._write_test_file(self.test_single_sheet_file, self.content1)

    def test_delete_sheets(self):
        b1 = pe.readers.Book(self.testfile)
        assert len(b1.sheet_names()) == 3
        del b1["Sheet1"]
        assert len(b1.sheet_names()) == 2
        try:
            del b1["Sheet1"]
            assert 1==2
        except KeyError:
            assert 1==1
        del b1[1]
        assert len(b1.sheet_names()) == 1
        try:
            del b1[1]
            assert 1==2
        except IndexError:
            assert 1==1
        try:
            del b1[1.1]
            assert 1==2
        except TypeError:
            assert 1==1
            
    def test_delete_sheets2(self):
        """repetitively delete first sheet"""
        b1 = pe.readers.Book(self.testfile)
        del b1[0]
        assert len(b1.sheet_names()) == 2
        del b1[0]
        assert len(b1.sheet_names()) == 1
        del b1[0]
        assert len(b1.sheet_names()) == 0
        
    def test_add_book1(self):
        """
        test this scenario: book3 = book1 + book2
        """
        b1 = pe.BookReader(self.testfile)
        b2 = pe.BookReader(self.testfile2)
        b3 = b1 + b2
        content = pe.utils.to_dict(b3)
        sheet_names = content.keys()
        assert len(sheet_names) == 6
        for name in sheet_names:
            if "Sheet3" in name:
                assert content[name] == self.content["Sheet3"]
            elif "Sheet2" in name:
                assert content[name] == self.content["Sheet2"]
            elif "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]
        
    def test_add_book1_in_place(self):
        """
        test this scenario: book1 +=  book2
        """
        b1 = pe.BookReader(self.testfile)
        b2 = pe.BookReader(self.testfile2)
        b1 += b2
        content = pe.utils.to_dict(b1)
        sheet_names = content.keys()
        assert len(sheet_names) == 6
        for name in sheet_names:
            if "Sheet3" in name:
                assert content[name] == self.content["Sheet3"]
            elif "Sheet2" in name:
                assert content[name] == self.content["Sheet2"]
            elif "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]

    def test_add_book2(self):
        """
        test this scenario: book3 = book1 + sheet3
        """
        b1 = pe.BookReader(self.testfile)
        b2 = pe.BookReader(self.testfile2)
        b3 = b1 + b2["Sheet3"]
        content = pe.utils.to_dict(b3)
        sheet_names = content.keys()
        assert len(sheet_names) == 4
        for name in sheet_names:
            if "Sheet3" in name:
                assert content[name] == self.content["Sheet3"]
            elif "Sheet2" in name:
                assert content[name] == self.content["Sheet2"]
            elif "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]

    def test_add_book2_in_place(self):
        """
        test this scenario: book3 = book1 + sheet3
        """
        b1 = pe.BookReader(self.testfile)
        b2 = pe.BookReader(self.testfile2)
        b1 += b2["Sheet3"]
        content = pe.utils.to_dict(b1)
        sheet_names = content.keys()
        assert len(sheet_names) == 4
        for name in sheet_names:
            if "Sheet3" in name:
                assert content[name] == self.content["Sheet3"]
            elif "Sheet2" in name:
                assert content[name] == self.content["Sheet2"]
            elif "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]

    def test_add_book3(self):
        """
        test this scenario: book3 = sheet1 + sheet2
        """
        b1 = pe.BookReader(self.testfile)
        b2 = pe.BookReader(self.testfile2)
        b3 = b1["Sheet1"] + b2["Sheet3"]
        content = pe.utils.to_dict(b3)
        sheet_names = content.keys()
        assert len(sheet_names) == 2
        assert content["Sheet3"] == self.content["Sheet3"]
        assert content["Sheet1"] == self.content["Sheet1"]
        
    def test_add_book4(self):
        """
        test this scenario: book3 = sheet1 + book
        """
        b1 = pe.BookReader(self.testfile)
        b2 = pe.BookReader(self.testfile2)
        b3 = b1["Sheet1"] + b2
        content = pe.utils.to_dict(b3)
        sheet_names = content.keys()
        assert len(sheet_names) == 4
        for name in sheet_names:
            if "Sheet3" in name:
                assert content[name] == self.content["Sheet3"]
            elif "Sheet2" in name:
                assert content[name] == self.content["Sheet2"]
            elif "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]

    def test_add_book5(self):
        """
        test this scenario: book3 = single_sheet_book + book
        """
        b1 = pe.BookReader(self.test_single_sheet_file)
        b2 = pe.BookReader(self.testfile2)
        b3 = b1 + b2
        content = pe.utils.to_dict(b3)
        sheet_names = content.keys()
        assert len(sheet_names) == 4
        for name in sheet_names:
            if "Sheet3" in name:
                assert content[name] == self.content["Sheet3"]
            elif "Sheet2" in name:
                assert content[name] == self.content["Sheet2"]
            elif "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]
            elif "single.xls" in name:
                assert content[name] == self.content1["Sheet1"]

    def test_add_book6(self):
        """
        test this scenario: book3 = book + single_sheet_book
        """
        b1 = pe.BookReader(self.test_single_sheet_file)
        b2 = pe.BookReader(self.testfile2)
        b3 = b2 + b1
        content = pe.utils.to_dict(b3)
        sheet_names = content.keys()
        assert len(sheet_names) == 4
        for name in sheet_names:
            if "Sheet3" in name:
                assert content[name] == self.content["Sheet3"]
            elif "Sheet2" in name:
                assert content[name] == self.content["Sheet2"]
            elif "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]
            elif "single.xls" in name:
                assert content[name] == self.content1["Sheet1"]

    def test_add_sheet(self):
        """
        test this scenario: book3 = sheet1 + single_sheet_book
        """
        b1 = pe.BookReader(self.testfile)
        b2 = pe.BookReader(self.test_single_sheet_file)
        b3 = b1["Sheet1"] + b2
        content = pe.utils.to_dict(b3)
        sheet_names = content.keys()
        assert len(sheet_names) == 2
        for name in sheet_names:
            if "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]
            elif "single.xls" in name:
                assert content[name] == self.content1["Sheet1"]

    def test_add_sheet2(self):
        """
        test this scenario: book3 = sheet1 + single_sheet_book
        """
        b1 = pe.BookReader(self.testfile)
        b3 = b1["Sheet1"] + b1["Sheet1"]
        content = pe.utils.to_dict(b3)
        sheet_names = content.keys()
        assert len(sheet_names) == 2
        for name in sheet_names:
            if "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]

    def test_add_book_error(self):
        """
        test this scenario: book3 = book + integer
        """
        b1 = pe.BookReader(self.testfile)
        try:
            b1 + 12
            assert 1==2
        except TypeError:
            assert 1==1
        try:
            b1 += 12
            assert 1==2
        except TypeError:
            assert 1==1

    def test_add_sheet_error(self):
        """
        test this scenario: book3 = sheet1 + integer
        """
        b1 = pe.BookReader(self.testfile)
        try:
            b1["Sheet1"] + 12
            assert 1==2
        except TypeError:
            assert 1==1
        try:
            b1["Sheet1"] += 12
            assert 1==2
        except TypeError:
            assert 1==1
        try:
            b1["Sheet1"] += pe.sheets.AS_COLUMNS(12)
            assert 1==2
        except TypeError:
            assert 1==1

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)
        if os.path.exists(self.testfile3):
            os.unlink(self.testfile3)
        if os.path.exists(self.test_single_sheet_file):
            os.unlink(self.test_single_sheet_file)


class TestMergeCSVsIntoOne:
    """
    This test case tests this code works
    >>> import pyexcel as pe
    >>> import glob
    >>> merged = pe.Reader()
    >>> for file in glob.glob("*.csv"):
    >>>     merged += pe.Reader(file)
    >>> writer = pe.Writer("merged.csv")
    >>> writer.write_reader(merged)
    >>> writer.close()
    """

    def test_merging(self):
        # set up
        data = [[1,2,3],[4,5,6],[7,8,9]]
        import pyexcel as pe
        w=pe.Writer("1.csv")
        w.write_rows(data)
        w.close()
        data2 = [['a','b','c'],['d','e','f'],['g','h','i']]
        w=pe.Writer("2.csv")
        w.write_rows(data2)
        w.close()
        data3=[[1.1, 2.2, 3.3],[4.4, 5.5, 6.6],[7.7, 8.8, 9.9]]
        w=pe.Writer("3.csv")
        w.write_rows(data3)
        w.close()
        # execute
        merged = pe.Reader()
        for file in ["1.csv", "2.csv", "3.csv"]:
            r = pe.Reader(file)
            merged += r
        writer = pe.Writer("merged.csv")
        writer.write_reader(merged)
        writer.close()
        r=pe.Reader("merged.csv")
        actual = pe.utils.to_array(r)
        result = [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
            ['a', 'b', 'c'],
            ['d', 'e', 'f'],
            ['g', 'h', 'i'],
            [1.1, 2.2, 3.3],
            [4.4, 5.5, 6.6],
            [7.7, 8.8, 9.9]
        ]
        assert result == actual
        # verify
        os.unlink("1.csv")
        os.unlink("2.csv")
        os.unlink("3.csv")
        os.unlink("merged.csv")
        


