# pyexcel [![Build Status](https://api.travis-ci.org/chfw/pyexcel.png)](http://travis-ci.org/chfw/pyexcel) [![codecov.io](https://codecov.io/github/chfw/pyexcel/coverage.png)](https://codecov.io/github/chfw/pyexcel)

Python Wrapper for reading and writing uniform distributed data table in csv, ods, xls, xlsx and xlsm files


## Example

Suppose you have a csv, xls, xlsx file as the following:

```
1,2,3 <- row starts at 0 -\
4,5,6                      > row_range()
7,8,9 <- number_of_rows()-/
^   ^
|   number_of_columns() -\
|                         > column_range()
column starts at 0      -/
```

The following code:

```python
import pyexcel

# "example.xls","example.xlsx","example.ods","example.xlsm"
spreadsheet = pyexcel.Reader("example.csv") 

for r in spreadsheet.row_range():
    for c in spreadsheet.column_range():
        print spreadsheet.cell_value(r, c)
```

will print them out as:

```
1
2
3
4
5
6
7
8
9
```

To get the same result above, you can iterate it through:

```python
import pyexcel

# "example.xls","example.xlsx","example.ods", "example.xlsm"
spreadsheet = pyexcel.Reader("example.csv") 

for value in spreadsheet:
    print value
```

And the following code:

```python
from pyexcel import Reader
from pyexcel.utils import to_array
import json

# "example.xls","example.xlsx","example.ods", "example.xlsm"
reader = Reader("example.csv")
data = to_array(reader.rows())
print json.dumps(data)
```

will print them out as json:

```
[["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
```

## Dependencies

* odfpy
* xlrd
* xlwt

## Note

ods reader is made by [Marco Conti](https://github.com/marcoconti83/read-ods-with-odfpy)