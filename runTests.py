from testFunParser import *
from testSaveLoad import *
from testRefine import *
import unittest

testSuite = unittest.makeSuite(testFunParser)
testSuite.addTest(unittest.makeSuite(testSaveLoad))
testSuite.addTest(unittest.makeSuit(testRefine))
#testSuite = unittest.makeSuite(testRefine)

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
