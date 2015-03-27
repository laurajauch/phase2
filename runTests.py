from testFunParser import *
import unittest

testSuite = unittest.makeSuite(testFunParser)

testRunner = unittest.TextTestRunner()
testRunner.run(testSuite)
