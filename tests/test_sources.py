from nose.tools import raises, eq_

from pyexcel.sources.factory import Source
from pyexcel.sources.factory import FileSource

from pyexcel.sources.file_source_output import WriteSheetToMemory
from pyexcel.sources.file_source_output import OutputSource
from pyexcel.sources.file_source_input import InputSource


def test_io_source():
    status = OutputSource.can_i_handle("read", "xls")
    eq_(status, False)


def test_input_source():
    status = InputSource.can_i_handle("write", "xls")
    eq_(status, False)


def test_source():
    source = Source(source="asource", params="params")
    assert source.keywords == {"params": "params"}
    assert source.source == "asource"


def test_source_class_method():
    assert Source.is_my_business('read', source="asource") is True
    assert Source.is_my_business('read', file_name="asource") is False


@raises(Exception)
def test_read_only_source():
    source = Source()
    source.write_data("something")


@raises(Exception)
def test_write_only_source():
    source = Source()
    source.get_data()


@raises(Exception)
def test_write_only_sheet_source():
    source = WriteSheetToMemory()
    source.get_data()


def test_file_source_class_method():
    assert FileSource.can_i_handle('read', "csv") is False
    assert FileSource.can_i_handle('write', "csv") is False
    assert FileSource.can_i_handle('wrong action', "csv") is False
