Data manipulation in a sheet
============================

The data in a sheet is represented by :class:`Matrix` which maintains the data as a list of lists. You can regard :class:`Matrix` as a two dimensional array with additional iterators. Random access to individual column and row is explosed by class:`Column` and class:`Row` 

Column manipulation with SeriesReader
-------------------------------------

Suppose have one data file as the following:

.. table:: file "example1.csv"

    ======== ======== ========
    Column 1 Column 2 Column 3
    ======== ======== ========
    1        4        7
    2        5        8
    3        6        9
    ======== ======== ========

And you want to update ``Column 2`` with these data: [11, 12, 13]

Here is the code::

    from pyexcel as pe

    reader = pe.SeriesReader("example1.csv")
    reader.column["Column 2"] = [11, 12, 13])
    writer = pe.Writer("output.xls")
    writer.write_reader(reader)
    writer.close()

Your output.xls will have these data:

.. table:: "output.xls"

    ======== ======== ========
    Column 1 Column 2 Column 3
    ======== ======== ========
    1        11       7
    2        12       8
    3        13       9
    ======== ======== ========

Remove one column of a data file
*********************************

If you want to remove ``Column 2``, you can just call::

    del reader.column["Column 2"]

Here is the code::

    from pyexcel as pe


    reader = pe.SeriesReader("example1.csv")
    del reader.column["Column 2"]
    writer = pe.Writer("output.xls")
    writer.write_reader(reader)
    writer.close()

Your output.xls will have these data:

.. table:: "output.xls"

    ======== ========
    Column 1 Column 3
    ======== ========
    1        7
    2        8
    3        9
    ======== ========


Append more columns to a data file
---------------------------------

Continue from previous example. Suppose you want add two more columns to the data file

======== ========
Column 4 Column 5
======== ========
10       13
11       14
12       15
======== ========

Here is the example code to append two extra columns::

    from pyexcel as pe

    reader = pe.SeriesReader("example1.csv")
    extra_data = [
        ["Column 4", "Column 5"],
        [10, 13],
        [11, 14],
        [12, 15]
    ]
    reader.column += extra_data
    writer = pe.Writer("output.xls")
    writer.write_reader(reader)
    writer.close()

Here is what you will get:

======== ======== ======== ======== ========
Column 1 Column 2 Column 3 Column 4 Column 5
======== ======== ======== ======== ========
1        11       7        10       13       
2        12       8        11       14       
3        13       9        12       15       
======== ======== ======== ======== ========

