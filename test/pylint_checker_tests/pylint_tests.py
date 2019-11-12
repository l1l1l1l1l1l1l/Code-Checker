# -*- coding: utf-8 -*-
# @Time    : 2019/11/5 17:17
# @Author  : LIU YUE
# @File    : pylint_tests.py.py

import unittest
from checker.pylintChecker.pylint import *


class TestUtils(unittest.TestCase):

    def test_pylint(self):
        grade, result = pylint("C:\\Users\\lynnl\\PycharmProjects\\Code-Checker\\test\\resources\\test_pylint_and_slc")
        self.assertIsNot(grade, 0)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
