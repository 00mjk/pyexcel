========
pyexcel 
========

.. image:: https://api.travis-ci.org/chfw/pyexcel.png
    :target: http://travis-ci.org/chfw/pyexcel

.. image:: https://codecov.io/github/chfw/pyexcel/coverage.png
    :target: https://codecov.io/github/chfw/pyexcel

.. image:: https://readthedocs.org/projects/pyexcel/badge/?version=latest
    :target: https://readthedocs.org/projects/pyexcel/?badge=latest

.. image:: https://pypip.in/d/pyexcel/badge.png
    :target: https://pypi.python.org/pypi/pyexcel

**pyexcel** is a wrapper library to read, manipulate and write data in different excel formats: csv, ods, xls, xlsx and xlsm. Its mission is to let you focus on data itself and it deals with different file formats. But this library does not support fonts, colors and charts. ODS format support is provided by pyexcel-ods and pyexcel-ods3.

It was created due to the lack of uniform programming interface to access data in different formats. A developer needs to use different methods of different libraries to read the same data in different excel formats, hence the resulting code is cluttered and unmaintainable.

All great work have done by odf, xlrd and other individual developers. This library unites only the data access code.

Installation
============
You can install it via pip::

    $ pip install pyexcel


or clone it and install it::


    $ git clone http://github.com/chfw/pyexcel.git
    $ cd pyexcel
    $ python setup.py install


Test 
====

Here is the test command::

    pip install -r tests/requirements.txt
    nosetests tests


Test coverage is shown in [codecov.io](https://codecov.io/github/chfw/pyexcel). You can get instant test coverage report by using the following command::

    nosetests tests --with-coverage --cover-package=pyexcel


Optionally, you can add `--cover-html --cover-html-dir=your_file_directory`

Known Issues
=============

* If a zero was typed in a DATE formatted field in xls, you will get "01/01/1900".
* If a zero was typed in a TIME formatted field in xls, you will get "00:00:00".

Documentation
=============

It is hosted in [pyhosted](https://pythonhosted.org/pyexcel/)

