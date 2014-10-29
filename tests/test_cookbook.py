import pyexcel as pe
import os
from base import clean_up_files


class TestSpliting:
    def setUp(self):
        self.testfile4 = "multiple_sheets.xls"
        self.content4 = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
        w = pe.BookWriter(self.testfile4)
        w.write_book_from_dict(self.content4)
        w.close()

    def test_split_a_book(self):
        pe.cookbook.split_a_book(self.testfile4, "extracted.csv")
        assert os.path.exists("Sheet1_extracted.csv")
        assert os.path.exists("Sheet2_extracted.csv")
        assert os.path.exists("Sheet3_extracted.csv")

    def test_split_a_book_2(self):
        """use default output file name"""
        pe.cookbook.split_a_book(self.testfile4)
        assert os.path.exists("Sheet1_%s" % self.testfile4)
        assert os.path.exists("Sheet2_%s" % self.testfile4)
        assert os.path.exists("Sheet3_%s" % self.testfile4)

    def test_extract_a_book(self):
        pe.cookbook.extract_a_sheet_from_a_book(self.testfile4, "Sheet1", "extracted.csv")
        assert os.path.exists("Sheet1_extracted.csv")

    def test_extract_a_book_2(self):
        """Use default output file name"""
        pe.cookbook.extract_a_sheet_from_a_book(self.testfile4, "Sheet1")
        assert os.path.exists("Sheet1_%s" % self.testfile4)

    def tearDown(self):
        file_list = [
            self.testfile4,
            "Sheet1_extracted.csv",
            "Sheet2_extracted.csv",
            "Sheet3_extracted.csv",
            "Sheet1_multiple_sheets.xls",
            "Sheet2_multiple_sheets.xls",
            "Sheet3_multiple_sheets.xls"]
        clean_up_files(file_list)


class TestCookbook:
    def setUp(self):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "test1.xls"
        self.content = {
            "X": [1, 2, 3, 4, 5],
            "Y": [6, 7, 8, 9, 10],
            "Z": [11, 12, 13, 14, 15],
        }
        w = pe.Writer(self.testfile)
        w.write_dict(self.content)
        w.close()
        self.testfile2 = "test.csv"
        self.content2 = {
            "O": [1, 2, 3, 4, 5],
            "P": [6, 7, 8, 9, 10],
            "Q": [11, 12, 13, 14, 15],
        }
        w = pe.Writer(self.testfile2)
        w.write_dict(self.content2)
        w.close()
        self.testfile3 = "test.xls"
        self.content3 = {
            "R": [1, 2, 3, 4, 5],
            "S": [6, 7, 8, 9, 10],
            "T": [11, 12, 13, 14, 15],
        }
        w = pe.Writer(self.testfile3)
        w.write_dict(self.content3)
        w.close()
        self.testfile4 = "multiple_sheets.xls"
        self.content4 = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
        w = pe.BookWriter(self.testfile4)
        w.write_book_from_dict(self.content4)
        w.close()

    def test_update_columns(self):
        bad_column = {"A": [31, 1, 1, 1, 1]}
        custom_column = {"Z": [33, 44, 55, 66, 77]}
        try:
            # try non-existent column first
            pe.cookbook.update_columns(self.testfile, bad_column)
            assert 1==2
        except ValueError:
            assert 1==1
        pe.cookbook.update_columns(self.testfile, custom_column)
        r = pe.SeriesReader("pyexcel_%s" % self.testfile)
        data = pe.utils.to_dict(r)
        assert data["Z"] == custom_column["Z"]
        try:
            # test if it try not overwrite a file
            pe.cookbook.update_columns(self.testfile, custom_column)
            r = pe.SeriesReader("pe_%s" % self.testfile)
            assert 1==2
        except NotImplementedError:
            assert 1==1
        pe.cookbook.update_columns(self.testfile, custom_column, "test4.xls")
        r = pe.SeriesReader("test4.xls")
        data = pe.utils.to_dict(r)
        assert data["Z"] == custom_column["Z"]

    def test_update_rows(self):
        bad_column = {100: [31, 1, 1, 1, 1]}
        custom_column = {1: [2,3,4]}
        try:
            # try non-existent column first
            pe.cookbook.update_rows(self.testfile, bad_column)
            assert 1==2
        except IndexError:
            assert 1==1
        pe.cookbook.update_rows(self.testfile, custom_column)
        r = pe.Reader("pyexcel_%s" % self.testfile)
        assert custom_column[1] == r.row_at(1)
        try:
            # try not to overwrite a file
            pe.cookbook.update_rows(self.testfile, custom_column)
            r = pe.SeriesReader("pyexcel_%s" % self.testfile)
            assert 1==2
        except NotImplementedError:
            assert 1==1
        pe.cookbook.update_rows(self.testfile, custom_column, "test4.xls")
        r = pe.Reader("test4.xls")
        assert custom_column[1] == r.row_at(1)

    def test_merge_two_files(self):
        pe.cookbook.merge_two_files(self.testfile, self.testfile2)
        r = pe.SeriesReader("pyexcel_merged.csv")
        r.format(pe.formatters.SheetFormatter(int))
        data = pe.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        assert data == content
        try:
            pe.cookbook.merge_two_files(self.testfile, self.testfile2)
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def test_merge_files(self):
        file_array = [self.testfile, self.testfile2, self.testfile3]
        pe.cookbook.merge_files(file_array)
        r = pe.SeriesReader("pyexcel_merged.csv")
        r.format(pe.formatters.SheetFormatter(int))
        data = pe.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        content.update(self.content3)
        assert data == content
        try:
            pe.cookbook.merge_files(file_array)
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def test_merge_two_readers(self):
        r1 = pe.SeriesReader(self.testfile)
        r2 = pe.SeriesReader(self.testfile2)
        pe.cookbook.merge_two_readers(r1, r2)
        r = pe.SeriesReader("pyexcel_merged.csv")
        r.format(pe.formatters.SheetFormatter(int))
        data = pe.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        assert data == content
        try:
            pe.cookbook.merge_two_readers(r1, r2)
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def test_merge_readers(self):
        r1 = pe.SeriesReader(self.testfile)
        r2 = pe.SeriesReader(self.testfile2)
        r3 = pe.SeriesReader(self.testfile3)
        file_array = [r1, r2, r3]
        pe.cookbook.merge_readers(file_array)
        r = pe.SeriesReader("pyexcel_merged.csv")
        r.format(pe.formatters.SheetFormatter(int))
        data = pe.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        content.update(self.content3)
        assert data == content
        try:
            pe.cookbook.merge_readers(file_array)
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def test_merge_two_row_filter_hat_readers(self):
        r1 = pe.SeriesReader(self.testfile)
        r2 = pe.SeriesReader(self.testfile2)
        pe.cookbook.merge_two_readers(r1, r2)
        r = pe.SeriesReader("pyexcel_merged.csv")
        r.format(pe.formatters.SheetFormatter(int))
        data = pe.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        assert data == content

    def test_merge_two_row_filter_hat_readers_2(self):
        """
        Now start row filtering
        """
        r1 = pe.SeriesReader(self.testfile)
        r1.add_filter(pe.filters.OddRowFilter())
        r2 = pe.SeriesReader(self.testfile2)
        r2.add_filter(pe.filters.EvenRowFilter())
        pe.cookbook.merge_two_readers(r1, r2)
        r = pe.SeriesReader("pyexcel_merged.csv")
        r.format(pe.formatters.SheetFormatter(int))
        data = pe.utils.to_dict(r)
        content = {
            'Y': [7, 9, 0],
            'X': [2, 4, 0],
            'Z': [12, 14, 0],
            'O': [1, 3, 5],
            'Q': [11, 13, 15],
            'P': [6, 8, 10]
        }
        assert data == content

    def test_merge_two_row_filter_hat_readers_3(self):
        """
        Now start column filtering
        """
        r1 = pe.SeriesReader(self.testfile)
        r1.add_filter(pe.filters.OddColumnFilter())
        r2 = pe.SeriesReader(self.testfile2)
        r2.add_filter(pe.filters.EvenColumnFilter())
        pe.cookbook.merge_two_readers(r1, r2)
        r = pe.SeriesReader("pyexcel_merged.csv")
        r.format(pe.formatters.SheetFormatter(int))
        data = pe.utils.to_dict(r)
        content = {
            "Y": [6, 7, 8, 9, 10],
            "O": [1, 2, 3, 4, 5],
            "Q": [11, 12, 13, 14, 15]
        }
        assert data == content

    def test_merge_any_files_to_a_book(self):
        file_array = [self.testfile, self.testfile2,
                      self.testfile3, self.testfile4]
        pe.cookbook.merge_all_to_a_book(file_array, "merged.xlsx")
        r = pe.BookReader("merged.xlsx")
        content = pe.utils.to_dict(r[self.testfile].become_series())
        assert content == self.content
        r[self.testfile2].format(pe.formatters.SheetFormatter(int))
        content2 = pe.utils.to_dict(r[self.testfile2].become_series())
        assert content2 == self.content2
        content3 = pe.utils.to_dict(r[self.testfile3].become_series())
        assert content3 == self.content3
        content4 = pe.utils.to_array(r["Sheet1"])
        assert content4 == self.content4["Sheet1"]
        content5 = pe.utils.to_array(r["Sheet2"])
        assert content5 == self.content4["Sheet2"]
        content6 = pe.utils.to_array(r["Sheet3"])
        assert content6 == self.content4["Sheet3"]

    def test_merge_csv_files_to_a_book(self):
        file_array = [self.testfile, self.testfile2,
                      self.testfile3]
        pe.cookbook.merge_csv_to_a_book(file_array, "merged.xlsx")
        r = pe.BookReader("merged.xlsx")
        content = pe.utils.to_dict(r[self.testfile].become_series())
        assert content == self.content
        r[self.testfile2].format(pe.formatters.SheetFormatter(int))
        content2 = pe.utils.to_dict(r[self.testfile2].become_series())
        assert content2 == self.content2
        content3 = pe.utils.to_dict(r[self.testfile3].become_series())
        assert content3 == self.content3

    def tearDown(self):
        file_list = [
            self.testfile,
            self.testfile2,
            self.testfile3,
            self.testfile4,
            "pyexcel_%s" % self.testfile,
            "pyexcel_merged.csv",
            "merged.xlsx",
            "merged.xls",
            "test4.xls"
        ]
        clean_up_files(file_list)