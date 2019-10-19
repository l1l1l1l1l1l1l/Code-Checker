import unittest
import os
import shutil
import zipfile
import os.path as p

from checker.repo_checker import repo

CURRENT = p.dirname(p.dirname(p.abspath(__file__)))
OUTPUT = p.join(CURRENT, 'resources/tmp')
REPO_PATH = p.join(OUTPUT, 'test_repo/')


class GitTests(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(OUTPUT):
            os.makedirs(OUTPUT)
        test_repo_resource = zipfile.ZipFile(p.join(CURRENT, 'resources/test_repo.zip'), 'r')
        for file in test_repo_resource.namelist():
            test_repo_resource.extract(file, OUTPUT)
        self.test_repo = repo.GitRepo(REPO_PATH)

    def tearDown(self):
        shutil.rmtree(OUTPUT, ignore_errors=True)

    def test_commit_info(self):
        right_result = [['2019-10-19', 7, 13]]
        self.assertEqual(right_result, self.test_repo.commit_info())

    def test_last_day(self):
        self.assertEqual('2019-02-28', repo.last_day('2019-03-01'))
        self.assertEqual('2016-02-29', repo.last_day('2016-03-01'))
