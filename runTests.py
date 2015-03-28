from testFunParser import *
from testSaveLoad import *
import unittest

testSuite = unittest.makeSuite(testFunParser)
testSuite.addTest(unittest.makeSuite(testSaveLoad))

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
