import unittest
import filecmp
import os
import shutil
import tarfile
import os.path as p

# from checker.cli import PARSER
from checker.vulns_checker.vulns import Check

RESOURCES = p.join(p.dirname(p.dirname(p.abspath(__file__))), 'resources/vulns/')
OUTPUT = p.join(RESOURCES, 'tmp/pydo/')
INPUTFILE = p.join(RESOURCES, 'pydo.tgz')

TESTRESULT = RESOURCES + 'test.html'
TRUERESULT = RESOURCES + 'true.html'


class VulnsTest(unittest.TestCase):

    def setUp(self):
        shutil.rmtree(OUTPUT, ignore_errors=True)
        os.makedirs(OUTPUT)
        pydoFiles = tarfile.open(INPUTFILE, "r:gz")
        pydoFiles.extractall(path=OUTPUT)
        Check(OUTPUT, 12722)


    def tearDown(self):
        shutil.rmtree(OUTPUT)
        os.remove(TESTRESULT)

    def testResult(self):
        if not os.path.isfile(TESTRESULT):
            self.fail("no output result file found")
        self.assertTrue(filecmp.cmp(TESTRESULT,TRUERESULT))



