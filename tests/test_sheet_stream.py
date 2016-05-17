from pyexcel.sources.file_source_output import WriteOnlySheetSource
from pyexcel.sheets import SheetStream
from pyexcel_io.manager import RWManager
from textwrap import dedent


def test_save_to():
    file_type = 'csv'
    io = RWManager.get_io(file_type)
    g = (i for i in [[1,2],[3,4]])
    ss = WriteOnlySheetSource(file_type=file_type, file_stream=io,
                              lineterminator='\n')
    sheet_stream = SheetStream("test", g)
    sheet_stream.save_to(ss)
    content = io.getvalue()
    expected = dedent("""\
    1,2
    3,4
    """)
    assert content == expected