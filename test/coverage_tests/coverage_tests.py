import unittest
import os
import shutil
import zipfile
import os.path as p

from checker.coverage_checker import cov

CURRENT = p.dirname(p.dirname(p.abspath(__file__)))
OUTPUT = p.join(CURRENT, 'resources/tmp')
REPO_PATH = p.join(OUTPUT, 'repo_for_coverage_test/')


class CoverageTests(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(OUTPUT):
            os.makedirs(OUTPUT)
        test_repo_resource = zipfile.ZipFile(p.join(CURRENT, 'resources/repo_for_coverage_test.zip'), 'r')
        for file in test_repo_resource.namelist():
            test_repo_resource.extract(file, OUTPUT)
        self.example = cov.Coverage(REPO_PATH)

    def tearDown(self):
        shutil.rmtree(OUTPUT, ignore_errors=True)

    def test_coverage_rate(self):
        self.assertEqual(73, int(self.example.coverage_rate() + 0.5))


if __name__ == '__main__':
    unittest.main()
