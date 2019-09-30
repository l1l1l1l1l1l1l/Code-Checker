import unittest
import os
import shutil
import zipfile
import os.path as p

from checker.repo_checker import repo

CURRENT = p.dirname(p.dirname(p.abspath(__file__)))
OUTPUT = p.join(CURRENT, 'resources/tmp')
REPO_PATH = p.join(OUTPUT, 'repo_for_test/')


class GitTests(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(OUTPUT):
            os.makedirs(OUTPUT)
        test_repo_resource = zipfile.ZipFile(p.join(CURRENT, 'resources/repo_for_test.zip'), 'r')
        for file in test_repo_resource.namelist():
            test_repo_resource.extract(file, OUTPUT)
        self.test_repo = repo.GitRepo(REPO_PATH)

    def tearDown(self):
        shutil.rmtree(OUTPUT, ignore_errors=True)

    def test_calculate_commits(self):
        right_result = [{'2019-09-30': 2}]
        self.assertEqual(right_result, self.test_repo.calculate_commits())
