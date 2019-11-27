import unittest
from checker.complexityChecker import complexity


class TestUtils(unittest.TestCase):

    def test_folder(self):
        dir = 'd:\mccabe'
        score = Test.get_score(dir)
        print('score: ' + str(score) + ' .')
        info = Test.get_complexity(dir)
        for line in info:
            print(line)
        print(Test.get_funcs_num(dir))

    def test_py(self):
        dir = 'd:\mccabe\mccabe.py'
        score = Test.get_score(dir)
        print('score: ' + str(score) + ' .')
        info = Test.get_complexity(dir)
        for line in info:
            print(line)
        print(Test.get_funcs_num(dir))
