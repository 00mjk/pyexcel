
"""
    pyexcel
    ~~~~~~~~~~~~~~~~~~~

    **pyexcel** is a wrapper library to read, manipulate and
    write data in different excel formats: csv, ods, xls, xlsx
    and xlsm. It does not support styling, charts.

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""

from .readers import Reader, BookReader
from .writers import Writer, BookWriter
from .readers import SeriesReader
import cookbook

__VERSION__ = '0.0.2'