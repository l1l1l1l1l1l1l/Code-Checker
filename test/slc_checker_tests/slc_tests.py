# -*- coding: utf-8 -*-
# @Time    : 2019/11/5 17:17
# @Author  : LIU YUE
# @File    : slc_tests.py.py

import unittest
from checker.slcChecker.slc import *


class TestUtils(unittest.TestCase):

    def test_slc(self):
        self.assertEqual(20, slc("C:\\Users\\lynnl\\PycharmProjects\\Code-Checker\\test\\resources\\test_pylint_and_slc"))


if __name__ == '__main__':
    unittest.main()
