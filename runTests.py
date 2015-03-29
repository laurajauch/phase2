from testFunParser import *
from testSaveLoad import *
from testRefine import *
from testInput import *
import unittest

testSuite = unittest.makeSuite(testFunParser)
testSuite.addTest(unittest.makeSuite(testSaveLoad))
testSuite.addTest(unittest.makeSuite(testRefine))
#testSuite = unittest.makeSuite(testRefine)
testSuite.addTest(unittest.makeSuite(testInput))

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
