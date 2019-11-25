import unittest
import filecmp
import os
import shutil
import tarfile
import os.path as p

# from checker.cli import PARSER
from checker.vulns_checker.vulns import Check

RESOURCES = p.join(
    p.dirname(p.dirname(p.abspath(__file__))), 'resources/vulns/')
OUTPUT = p.join(RESOURCES, 'tmp/pydo/')
INPUTFILE = p.join(RESOURCES, 'pydo.tgz')


class VulnsTest(unittest.TestCase):

    def setUp(self):
        shutil.rmtree(OUTPUT, ignore_errors=True)
        os.makedirs(OUTPUT)
        pydoFiles = tarfile.open(INPUTFILE, "r:gz")
        pydoFiles.extractall(path=OUTPUT)

    def tearDown(self):
        shutil.rmtree(OUTPUT)

    def testResult(self):
        self.assertEqual(Check(OUTPUT, 12722), 41)
