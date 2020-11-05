import random

from base import PyexcelSheetBase


class TestSheetAccess(PyexcelSheetBase):
    @staticmethod
    def get_random_char():
        i = random.randint(97, 122)
        return chr(i)

    def test_out_of_bounds_write(self):
        value = self.get_random_char()
        column = self.get_random_char() + self.get_random_char()
        cell = column + str(random.randint(1, 30))
        self.sheet[cell] = value

        self.assertEqual(value, self.sheet[cell])

    def test_out_of_bounds_read(self):
        with self.assertRaises(IndexError):
            self.sheet[0, 20]

        with self.assertRaises(IndexError):
            self.sheet[20, 0]
