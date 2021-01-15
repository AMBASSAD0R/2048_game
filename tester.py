# тесты логики

import unittest

from functions import enumerate_mas, is_empty, get_index_from_number, is_full, move_left, move_up, move_down


class MainTest(unittest.TestCase):

    def test_1(self):
        self.assertEqual(enumerate_mas(1, 2), 7)

    def test_2(self):
        self.assertEqual(enumerate_mas(3, 3), 16)

    def test_3(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        field = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertEqual(is_empty(field), a)

    def test_4(self):
        a = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        field = [
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertEqual(is_empty(field), a)

    def test_5(self):
        a = []
        field = [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
        self.assertEqual(is_empty(field), a)

    def test_6(self):
        self.assertEqual(get_index_from_number(7), (1, 2))

    def test_7(self):
        self.assertEqual(get_index_from_number(16), (3, 3))

    def test_8(self):
        self.assertEqual(get_index_from_number(1), (0, 0))

    def test_9(self):
        field = [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
        self.assertEqual(is_full(field), False)

    def test_10(self):
        field = [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 0, 1, 1],
            [1, 1, 1, 1],
        ]
        self.assertEqual(is_full(field), True)

    def test_11(self):
        field = [
            [0, 1, 1, 0],
            [1, 1, 0, 1],
            [1, 0, 1, 0],
            [1, 0, 0, 1],
        ]
        self.assertEqual(is_full(field), True)

    def test_12(self):
        field = [
            [2, 2, 0, 0],
            [0, 4, 4, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        res = [
            [4, 0, 0, 0],
            [8, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertEqual(move_left(field), (res, 12))

    def test_13(self):
        field = [
            [2, 4, 4, 2],
            [4, 0, 0, 2],
            [0, 0, 0, 0],
            [8, 8, 4, 4],
        ]
        res = [
            [2, 8, 2, 0],
            [4, 2, 0, 0],
            [0, 0, 0, 0],
            [16, 8, 0, 0],
        ]
        self.assertEqual(move_left(field), (res, 32))

    def test_15(self):
        field = [
            [2, 4, 0, 2],
            [2, 0, 2, 0],
            [4, 0, 2, 4],
            [4, 4, 0, 0],
        ]
        res = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [4, 0, 0, 2],
            [8, 8, 4, 4],
        ]
        self.assertEqual(move_down(field), res)


if __name__ == '__main__':
    unittest.main()
