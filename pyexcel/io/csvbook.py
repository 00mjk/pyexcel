import six
import csv
import codecs


class UTF8Recorder(six.Iterator):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8.
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
        
    def __iter__(self):
        return self
        
    def __next__(self):
        return next(self.reader).encode('utf-8')


class CSVBook:
    """
    CSVBook reader

    It simply return one sheet
    """
    def __init__(self, file, encoding="utf-8", **keywords):
        self.array = []
        if six.PY2:
            f = open(file, 'rb')
        elif six.PY3:
            f = open(file, 'rt')
        utf_reader = UTF8Recorder(f, encoding)
        reader = csv.reader(utf_reader, dialect=csv.excel, **keywords)
        longest_row_length = -1
        for row in reader:
            myrow = []
            for element in row:
                myrow.append(element.decode('utf-8'))
            if longest_row_length == -1:
                longest_row_length = len(myrow)
            elif longest_row_length < len(myrow):
                longest_row_length = len(myrow)
            self.array.append(myrow)
        if len(self.array) > 0:
            if len(self.array[0]) < longest_row_length:
                self.array[0] = self.array[0] + [""] * (longest_row_length - len(self.array[0]))
        self.mysheets = {
            "csv": self.array
        }

    def sheets(self):
        return self.mysheets


class CSVSheetWriter:
    """
    csv file writer

    """
    def __init__(self, file, name, encoding="utf-8", **keywords):
        if name:
            names = file.split(".")
            file_name = "%s_%s.%s" % (names[0], name, names[1])
        else:
            file_name = file

        if six.PY2:
            self.f = open(file_name, "wb")
        elif six.PY3:
            self.f = open(file_name, "w", newline="")
        self.encoding = encoding
        self.writer = csv.writer(self.f, **keywords)

    def set_size(self, size):
        pass

    def write_row(self, array):
        """
        write a row into the file
        """
        self.writer.writerow([six.text_type(s if s != None else '').encode(self.encoding) for s in array])

    def close(self):
        """
        This call close the file handle
        """
        self.f.close()


class CSVWriter:
    """
    csv file writer

    if there is multiple sheets for csv file, it simpily writes
    multiple csv files
    """
    def __init__(self, file, **keywords):
        self.file = file
        self.count = 0
        self.keywords = keywords

    def create_sheet(self, name):
        return CSVSheetWriter(self.file, name, **self.keywords)

    def close(self):
        """
        This call close the file handle
        """
        pass
