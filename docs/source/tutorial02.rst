
Sheet: Data filtering
======================

use :meth:`~pyexcel.Sheet.filter` function to apply a filter immediately. The content is modified.


Suppose you have the following data in any of the supported excel formats:

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        4        7
2        5        8
3        6        9
======== ======== ========

    >>> import pyexcel

.. testcode::
   :hide:

   >>> data = [
   ...      ["Column 1", "Column 2", "Column 3"],
   ...      [1, 2, 3],
   ...      [4, 5, 6],
   ...      [7, 8, 9]
   ...  ]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example_series.xls")

.. code-block:: python

    >>> sheet = pyexcel.get_sheet(file_name="example_series.xls", name_columns_by_row=0)
    >>> sheet.content
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +==========+==========+==========+
    | 1        | 2        | 3        |
    +----------+----------+----------+
    | 4        | 5        | 6        |
    +----------+----------+----------+
    | 7        | 8        | 9        |
    +----------+----------+----------+

Filter out some data
--------------------------

You may want to filter odd rows and print them in an array of dictionaries:

.. code-block:: python

    >>> sheet.filter(row_indices=[0, 2])
    >>> sheet.content
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +==========+==========+==========+
    | 4        | 5        | 6        |
    +----------+----------+----------+

Let's try to further filter out even columns:

.. code-block:: python

    >>> sheet.filter(column_indices=[1])
    >>> sheet.content
    +----------+----------+
    | Column 1 | Column 3 |
    +==========+==========+
    | 4        | 6        |
    +----------+----------+

Save the data
*************

Let's save the previous filtered data:

.. code-block:: python

    >>> sheet.save_as("example_series_filter.xls")

When you open `example_series_filter.xls`, you will find these data

======== ========
Column 1 Column 3
======== ========
2        8
======== ========

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("example_series_filter.xls")


How to filter out empty rows in my sheet?
**************************************************

Suppose you have the following data in a sheet and you want to remove those rows with blanks:

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.Sheet([[1,2,3],['','',''],['','',''],[1,2,3]])

You can use :class:`pyexcel.filters.RowValueFilter`, which examines each row, return `True` if the row should be filtered out. So, let's define a filter function:

.. code-block:: python

    >>> def filter_row(row_index, row):
    ...     result = [element for element in row if element != '']
    ...     return len(result)==0


And then apply the filter on the sheet:

.. code-block:: python

    >>> del sheet.row[filter_row]
    >>> sheet
    pyexcel sheet:
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+

   

Work with multi-sheet file
--------------------------

How do I read a book, process it and save to a new book
******************************************************

Yes, you can do that. The code looks like this::

   import pyexcel

   book = pyexcel.get_book(file_name="yourfile.xls")
   for sheet in book:
       # do you processing with sheet
       # do filtering?
       pass
   book.save_as("output.xls")
 
What would happen if I save a multi sheet book into "csv" file
**************************************************************

Well, you will get one csv file per each sheet. Suppose you have these code:

.. code-block:: python

   >>> content = {
   ...     'Sheet 1': 
   ...         [
   ...             [1.0, 2.0, 3.0], 
   ...             [4.0, 5.0, 6.0], 
   ...             [7.0, 8.0, 9.0]
   ...         ],
   ...     'Sheet 2': 
   ...         [
   ...             ['X', 'Y', 'Z'], 
   ...             [1.0, 2.0, 3.0], 
   ...             [4.0, 5.0, 6.0]
   ...         ], 
   ...     'Sheet 3': 
   ...         [
   ...             ['O', 'P', 'Q'], 
   ...             [3.0, 2.0, 1.0], 
   ...             [4.0, 3.0, 2.0]
   ...         ] 
   ... }
   >>> book = pyexcel.Book(content)
   >>> book.save_as("myfile.csv")

You will end up with three csv files:

.. code-block:: python

   >>> import glob
   >>> outputfiles = glob.glob("myfile_*.csv")
   >>> for file in sorted(outputfiles):
   ...     print(file)
   ...
   myfile__Sheet 1__0.csv
   myfile__Sheet 2__1.csv
   myfile__Sheet 3__2.csv

and their content is the value of the dictionary at the corresponding key


After I have saved my multiple sheet book in csv format, how do I get them back in pyexcel
*******************************************************************************************

First of all, you can read them back individual as csv file using `meth:~pyexcel.get_sheet` method. Secondly, the pyexcel can do
the magic to load all of them back into a book. You will just need to provide the common name before the separator "__":

.. code-block:: python

    >>> book2 = pyexcel.get_book(file_name="myfile.csv")
    >>> book2
    Sheet 1:
    +-----+-----+-----+
    | 1.0 | 2.0 | 3.0 |
    +-----+-----+-----+
    | 4.0 | 5.0 | 6.0 |
    +-----+-----+-----+
    | 7.0 | 8.0 | 9.0 |
    +-----+-----+-----+
    Sheet 2:
    +-----+-----+-----+
    | X   | Y   | Z   |
    +-----+-----+-----+
    | 1.0 | 2.0 | 3.0 |
    +-----+-----+-----+
    | 4.0 | 5.0 | 6.0 |
    +-----+-----+-----+
    Sheet 3:
    +-----+-----+-----+
    | O   | P   | Q   |
    +-----+-----+-----+
    | 3.0 | 2.0 | 1.0 |
    +-----+-----+-----+
    | 4.0 | 3.0 | 2.0 |
    +-----+-----+-----+
    
.. testcode::
   :hide:

   >>> os.unlink("myfile__Sheet 1__0.csv")
   >>> os.unlink("myfile__Sheet 2__1.csv")
   >>> os.unlink("myfile__Sheet 3__2.csv")
   >>> os.unlink("example_series.xls")
