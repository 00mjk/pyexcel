Migrate from 0.2.x to 0.3.0
================================

`pyexcel.sheets` are simplified. Soft filtering and formatting are gone. if you use
one of the following functions:

#. add_formatter
#. remove_fomatter
#. clear_formatters
#. freeze_formatters
#. add_filter
#. remove_filter
#. clear_filters
#. freeze_formatters

Please use apply_formatter and apply_filter instead


Migrate from 0.2.1 to 0.2.2+
================================

1. Explicit imports, no longer needed
--------------------------------------------

Please forget about these statements::

    import pyexcel.ext.xls
    import pyexcel.ext.ods
    import pyexcel.ext.xlsx

They are no longer needed. As long as you have pip-installed them, they will
be auto-loaded. However, if you do not want some of the plugins, please use
`pip` to uninstall them.

What if you have your code as it is? No harm but a few warnings shown::

    Deprecated usage since v0.2.2! Explicit import is no longer required. pyexcel.ext.ods is auto imported.


2. Invalid environment marker: platform_python_implementation=="PyPy"
-----------------------------------------------------------------------

Yes, it is a surprise. Please upgrade setuptools in your environment::

    pip install --upgrade setuptools

At the time of writing, setuptools (18.0.1) or setuptools-21.0.0-py2.py3-none-any.whl is installed on author's computer and worked.


3. How to keep both pyexcel-xls and pyexcel-xlsx
----------------------------------------------------------------

As in `Issue 20 <https://github.com/pyexcel/pyexcel/issues/20>`_, pyexcel-xls was used for xls and pyexcel-xlsx had to be used for xlsx. Both must co-exist due to requirements. The workaround would failed when auto-import are enabled in v0.2.2. Hence, user of pyexcel in this situation shall use 'library' parameter to all signature functions, to instruct pyexcel to use a named library for each function call.

4. pyexcel.get_io is no longer exposed
--------------------------------------------------------------

pyexcel.get_io was passed on from pyexcel-io. However, it is no longer exposed. Please use pyexcel_io.manager.RWManager.get_io if you have to.

You are likely to use pyexcel.get_io when you do :meth:`pyexcel.Sheet.save_to_memory` or :meth:`pyexcel.Book.save_to_memory` where you need to put in a io stream. But actually,
with latest code, you could put in a `None`.

Migrate from 0.1.x to 0.2.x
===============================

1. "Writer" is gone, Please use save_as.
-------------------------------------------

.. testcode::
   :hide:

    >>> import pyexcel

Here is a piece of legacy code:

.. code-block:: python

    w = pyexcel.Writer("afile.csv")
    data=[['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]]
    w.write_array(table)
    w.close()

The new code is:

.. code-block:: python

    >>> data=[['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]]
    >>> pyexcel.save_as(array=data, dest_file_name="afile.csv")

.. testcode::
   :hide:

    >>> import os
    >>> os.unlink("afile.csv")


Here is another piece of legacy code:

.. code-block:: python

    content = {
        "X": [1,2,3,4,5],
        "Y": [6,7,8,9,10],
        "Z": [11,12,13,14,15],
    }
    w = pyexcel.Writer("afile.csv")
    w.write_dict(self.content)
    w.close()

The new code is:

.. code-block:: python

   >>> content = {
   ...     "X": [1,2,3,4,5],
   ...     "Y": [6,7,8,9,10],
   ...     "Z": [11,12,13,14,15],
   ... }
   >>> pyexcel.save_as(adict=content, dest_file_name="afile.csv")

   
.. testcode::
   :hide:

    >>> import os
    >>> os.unlink("afile.csv")

Here is yet another piece of legacy code:

.. code-block:: python

    data = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    io = StringIO()
    w = pyexcel.Writer(("csv",io))
    w.write_rows(data)
    w.close()

The new code is:

    
    >>> data = [
    ...     [1, 2, 3],
    ...     [4, 5, 6]
    ... ]
    >>> io = pyexcel.save_as(dest_file_type='csv', array=data)
    >>> for line in io.readlines():
    ...     print(line.rstrip())
    1,2,3
    4,5,6
    
2. "BookWriter" is gone. Please use save_book_as.
---------------------------------------------------

Here is a piece of legacy code:

.. code-block:: python

   import pyexcel
   content = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
   w = pyexcel.BookWriter("afile.csv")
   w.write_book_from_dict(content)
   w.close()


The replacement code is:

.. code-block:: python

   >>> import pyexcel
   >>> content = {
   ...          "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
   ...          "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
   ...          "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
   ...      }
   >>> pyexcel.save_book_as(bookdict=content, dest_file_name="afile.csv")

.. testcode::
   :hide:

    >>> import os
    >>> os.unlink("afile__Sheet1__0.csv")
    >>> os.unlink("afile__Sheet2__1.csv")
    >>> os.unlink("afile__Sheet3__2.csv")

