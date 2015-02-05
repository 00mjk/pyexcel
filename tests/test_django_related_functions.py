import pyexcel as pe
import pyexcel.ext.xls
import os
from db import Session, Base, Signature, Signature2, engine
from _compact import OrderedDict
from nose.tools import raises


class Objects:
    def __init__(self):
        self.objs = None
        
    def bulk_create(self, objs, batch_size):
        self.objs = objs
        self.batch_size = batch_size

class FakeDjangoModel:
    def __init__(self):
        self.objects = Objects()

    def __call__(self, **keywords):
        return keywords


class TestExceptions:
    @raises(NameError)
    def test_sheet_save_to_django_model(self):
        model=FakeDjangoModel()
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        sheet = pe.Sheet(data)
        sheet.save_to_django_model(model)
        assert model.objects.objs == data

    @raises(NameError)
    def test_module_save_to_django_model(self):
        model=FakeDjangoModel()
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        pe.save_as(array=data, dest_model=model)
        assert model.objects.objs == data

    @raises(NameError)
    def test_book_save_to_models(self):
        model=FakeDjangoModel()
        content = OrderedDict()
        content.update({"Sheet1": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]})
        book = pe.Book(content)
        book.save_to_django_models([model])
        assert model.objects.objs == self.result


class TestSheet:
    def setUp(self):
        self.data  = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        self.result = [
            {'Y': 2, 'X': 1, 'Z': 3},
            {'Y': 5, 'X': 4, 'Z': 6}
        ]
        
    def test_sheet_save_to_django_model(self):
        model=FakeDjangoModel()
        sheet = pe.Sheet(self.data, name_columns_by_row=0)
        sheet.save_to_django_model(model)
        assert model.objects.objs == self.result

    def test_sheet_save_to_django_model_2(self):
        model=FakeDjangoModel()
        sheet = pe.Sheet(self.data)
        sheet.save_to_django_model((model, None, None, 0))
        assert model.objects.objs == self.result

    def test_model_save_to_django_model(self):
        model=FakeDjangoModel()
        pe.save_as(array=self.data, name_columns_by_row=0, dest_model=model)
        assert model.objects.objs == self.result

    def test_model_save_to_django_model_2(self):
        model=FakeDjangoModel()
        pe.save_as(array=self.data, dest_model=(model, None, None, 0))
        assert model.objects.objs == self.result

class TestBook:
    def setUp(self):
        self.content = OrderedDict()
        self.content.update({"Sheet1": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]})
        self.result = [{'Y': 4, 'X': 1, 'Z': 7}, {'Y': 5, 'X': 2, 'Z': 8}, {'Y': 6, 'X': 3, 'Z': 9}]

    def test_book_save_to_models(self):
        model=FakeDjangoModel()
        book = pe.Book(self.content)
        book.save_to_django_models([(model, None, None, 0)])
        assert model.objects.objs == self.result
