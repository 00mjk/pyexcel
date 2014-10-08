import pyexcel
import os
import datetime


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
        w = pyexcel.Writer(self.testfile)
        data=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
        w.write_row(data[:4])
        w.write_row(data[4:8])
        w.write_row(data[8:12])
        w.close()

    def test_update_a_cell(self):
        r = pyexcel.readers.PlainReader(self.testfile)
        r.cell_value(0,0,'k')
        assert r[0][0] == 'k'
        d = datetime.date(2014, 10, 1)
        r.cell_value(0,1,d)
        assert isinstance(r[0][1], datetime.date) is True
        assert r[0][1].strftime("%d/%m/%y") == "01/10/14"

    def test_update_a_cell_with_a_filter(self):
        """
        Filter the sheet first and then update the filtered now

        with the filter, you can set its value. then clear
        the filters, the value stays with the cell. so if you want
        to save the change with original data, please clear the filter
        first
        """
        r = pyexcel.FilterableReader(self.testfile)
        r.filter(pyexcel.filters.ColumnFilter([0, 2]))
        r.cell_value(2, 1, "k")
        assert r[2][1] == "k"
        r.clear_filters()
        assert r[2][3] == "k"

    def test_set_item(self):
        r = pyexcel.Reader(self.testfile)
        content = ['r', 's', 't', 'o']
        r[1] = content
        assert r[1] == ['r', 's', 't', 'o']
        content2 = [1, 2, 3, 4]
        r[1:] = content2
        assert r[2] == [1, 2, 3, 4]
        content3 = [True, False, True, False]
        r[0:0] = content3
        assert r[0] == [True, False, True, False]
        r[0:2:1] = [1, 1, 1, 1]
        assert r[0] == [1, 1, 1, 1]
        assert r[1] == [1, 1, 1, 1]
        assert r[2] == [1, 2, 3, 4]
        try:
            r[2:1] = ['e', 'r', 'r', 'o']
            assert 1==2
        except ValueError:
            assert 1==1

    def test_delete_item(self):
        r = pyexcel.readers.PlainReader(self.testfile)
        content = ['i', 'j', 1.1, 1]
        assert r[2] == content
        del r[0]
        assert r[1] == content
        r2 = pyexcel.readers.PlainReader(self.testfile)
        del r2[1:]
        assert r2.number_of_rows() == 1
        r3 = pyexcel.readers.PlainReader(self.testfile)
        del r3[0:0]
        assert r3[1] == content
        assert r3.number_of_rows() == 2
        try:
            del r[2:1]
            assert 1==2
        except ValueError:
            assert 1==1

    def test_extend_rows(self):
        r = pyexcel.PlainReader(self.testfile)
        content = [['r', 's', 't', 'o'],
                   [1, 2, 3, 4],
                   [True],
                   [1.1, 2.2, 3.3, 4.4, 5.5]]
        r.extend_rows(content)
        assert r[3] == ['r', 's', 't', 'o']
        assert r[4] == [1, 2, 3, 4]
        assert r[5] == [True, "", "", ""]
        assert r[6] == [1.1, 2.2, 3.3, 4.4]
        r2 = pyexcel.PlainReader(self.testfile)
        r2 += content
        assert r2[3] == ['r', 's', 't', 'o']
        assert r2[4] == [1, 2, 3, 4]
        assert r2[5] == [True, "", "", ""]
        assert r2[6] == [1.1, 2.2, 3.3, 4.4]        
        r3 = pyexcel.PlainReader(self.testfile)
        sheet = pyexcel.sheets.Sheet(content, "test")
        r3 += sheet
        assert r3[3] == ['r', 's', 't', 'o']
        assert r3[4] == [1, 2, 3, 4]
        assert r3[5] == [True, "", "", ""]
        assert r3[6] == [1.1, 2.2, 3.3, 4.4]
        try:
            r3 += 12
            assert 1==2
        except ValueError:
            assert 1==1
        try:
            r2 = pyexcel.Reader(self.testfile)
            content = [['r', 's', 't', 'o'],
                       [1, 2, 3, 4],
                       [True],
                       [1.1, 2.2, 3.3, 4.4, 5.5]]
            r2.extend_rows(content)
            assert 1==2
        except NotImplementedError:
            assert 1==1
            
    def test_extend_columns(self):
        r = pyexcel.PlainReader(self.testfile)
        columns = [['c1', 'c2', 'c3'],
                   ['x1', 'x2', 'x4']]
        r.extend_columns(columns)
        assert r[0] == ['a', 'b', 'c', 'd', 'c1', 'c2', 'c3']
        assert r[1] == ['e', 'f', 'g', 'h', 'x1', 'x2', 'x4']
        assert r[2] == ['i', 'j', 1.1, 1, '', '', '']
        r2 = pyexcel.PlainReader(self.testfile)
        columns2 = [['c1', 'c2', 'c3'],
                   ['x1', 'x2', 'x4'],
                   ['y1', 'y2'],
                   ['z1']]
        r2.extend_columns(columns2)
        assert r2[0] == ['a', 'b', 'c', 'd', 'c1', 'c2', 'c3']
        assert r2[1] == ['e', 'f', 'g', 'h', 'x1', 'x2', 'x4']
        assert r2[2] == ['i', 'j', 1.1, 1, 'y1', 'y2', '']
        assert r2[3] == ['', '', '', '', 'z1', '', '']
        try:
            r2 = pyexcel.Reader(self.testfile)
            r2.extend_columns(columns2)
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def test_add_as_columns(self):
        # test += operator
        columns2 = [['c1', 'c2', 'c3'],
                   ['x1', 'x2', 'x4'],
                   ['y1', 'y2'],
                   ['z1']]
        r3 = pyexcel.PlainReader(self.testfile)
        r3 += pyexcel.sheets.AS_COLUMNS(columns2)
        assert r3[0] == ['a', 'b', 'c', 'd', 'c1', 'c2', 'c3']
        assert r3[1] == ['e', 'f', 'g', 'h', 'x1', 'x2', 'x4']
        assert r3[2] == ['i', 'j', 1.1, 1, 'y1', 'y2', '']
        assert r3[3] == ['', '', '', '', 'z1', '', '']
        r4 = pyexcel.PlainReader(self.testfile)
        sheet = pyexcel.sheets.Sheet(columns2, "test")
        r4 += pyexcel.sheets.AS_COLUMNS(sheet)
        assert r4[0] == ['a', 'b', 'c', 'd', 'c1', 'c2', 'c3']
        assert r4[1] == ['e', 'f', 'g', 'h', 'x1', 'x2', 'x4']
        assert r4[2] == ['i', 'j', 1.1, 1, 'y1', 'y2', '']
        assert r4[3] == ['', '', '', '', 'z1', '', '']

    def test_set_column_at(self):
        r = pyexcel.PlainReader(self.testfile)
        try:
            r.set_column_at(1,[11,1], 1000)
            assert 1==2
        except ValueError:
            assert 1==1
            
    def test_delete_rows(self):
        r = pyexcel.PlainReader(self.testfile)
        r.delete_rows([0,1])
        assert r[0] == ['i', 'j', 1.1, 1]
        try:
            r.delete_rows("hi")
            assert 1==2
        except ValueError:
            assert 1==1
        try:
            r2 = pyexcel.Reader(self.testfile)
            r2.delete_rows([1,2])
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def test_delete_columns(self):
        r = pyexcel.PlainReader(self.testfile)
        r.delete_columns([0,2])
        assert r[0] == ['b', 'd']
        try:
            r.delete_columns("hi")
            assert 1==2
        except ValueError:
            assert 1==1
        try:
            r2 = pyexcel.Reader(self.testfile)
            r2.delete_columns([1,2])
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
