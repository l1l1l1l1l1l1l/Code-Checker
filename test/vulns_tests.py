import unittest
import filecmp
import os
import shutil
import tarfile
import os.path as p

from checker.cli import PARSER
from checker.vulnsChecker.vulns import main

RESOURCES = p.join(p.dirname(p.abspath(__file__)), 'resources')
OUTPUT = p.join(RESOURCES, 'tmp/pydo/')
INPUTFILE = p.join(RESOURCES, 'pydo.tgz')

TESTRESULT = p.dirname(p.abspath(__file__)) + '/testResult.html'
TRUERESULT = p.dirname(p.abspath(__file__)) + '/trueResult.html'


class VulnsTest(unittest.TestCase):

    def setUp(self):
        shutil.rmtree(OUTPUT, ignore_errors=True)
        os.makedirs(OUTPUT)
        pydoFiles = tarfile.open(INPUTFILE, "r:gz")
        pydoFiles.extractall(path=OUTPUT)
        args = PARSER.parse_args(['vulns','-q','-r','-f','html','-o',TESTRESULT,'OUTPUT'])
        try: 
            main(args)
        except:
            pass    

    def tearDown(self):
        shutil.rmtree(OUTPUT)
        os.remove(TESTRESULT)

    def testResult(self):
        if not os.path.isfile(TESTRESULT):
            self.fail("no output result file existing")
        self.assertTrue(filecmp.cmp(TESTRESULT,TRUERESULT))



