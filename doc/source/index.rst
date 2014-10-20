.. pyexcel documentation master file, created by
   sphinx-quickstart on Tue Sep  9 08:53:12 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

`pyexcel` - Let you focus on data, instead of file formats
==========================================================

:Author: C.W.
:Source code: http://github.com/chfw/pyexcel
:Issues: http://github.com/chfw/pyexcel/issues
:License: GPL v3
:Version: 0.0.5

Introduction
-------------

**pyexcel** is a wrapper library to read, manipulate and write data in different excel formats: csv, ods, xls, xlsx and xlsm. The data in excel files can be turned into array or dict with least code, and vice versa. And ready-made or custom filters and formatters can be applied. But it does not support fonts, colors and charts.

It was created due to the lack of uniform programming interface to access data in different excel formats. A developer needs to use different methods of different libraries to read the same data in different excel formats, hence the resulting code is cluttered and unmaintainable.

All great work have done by odf, xlrd and other individual developers. This library unites only the data access code.


Installation
-------------

You can install it via pip::

    $ pip install pyexcel


Getting the source
-------------------

Source code is hosted in github. You can get it using git client::

    $ git clone http://github.com/chfw/pyexcel.git


Open Document Spreadsheet(ods) Support
-----------------------------------------

In order to add ods support, please choose one of two packages: `pyexcel-ods <https://github.com/chfw/pyexcel-ods>`_ or `pyexcel-ods3 <https://github.com/chfw/pyexcel-ods3>`_ ::

    $ pip install pyexcel-ods

or::

    $ pip install pyexcel-ods3

In order to use them together with `pyexcel`, you need an extra import line in your code to activate it::

    from pyexcel.ext import ods

or::

    from pyexcel.ext import ods3

No futher code is needed. `pyexcel` will automatically support *ods* after this import.

Here is the comparsion of two packages:

============ ========== ========== ========== ========== ==============
package      python 2.6 python 2.7 python 3.3 python 3.4 lxml dependent
============ ========== ========== ========== ========== ==============
pyexcel-ods  yes	    yes	   	   						 no   		  
pyexcel-ods3 		    yes        yes        yes		 yes		      		   	 		   
============ ========== ========== ========== ========== ============== 

Usage examples
----------------

Tutorial
+++++++++

.. toctree::

    tutorial
	tutorial05
    tutorial02
    tutorial03
    tutorial04

Cook book
++++++++++

.. toctree::

    cookbook

API documentation
++++++++++++++++++

.. toctree::

    pyexcel

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

