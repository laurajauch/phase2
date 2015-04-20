from solver import *
from PyCamellia import *
import unittest

class testFunParser(unittest.TestCase):

    def testBasic(self):
        x = Solver(True)
        y = x.functionParser("-3*(y-1)*(y-2)")
        yVar = Function.yn(1)
        z = -3 * (yVar-1)*(yVar-2)
        self.assertAlmostEqual(z.evaluate(2,2), y.evaluate(2,2), delta=1e-12)

    def testBasicRoberts(self):
        mySolver = Solver(True)
        f_actual = mySolver.functionParser("-3*(y-1)*(y-2)")
        y = Function.yn(1)
        f_expected = -3*(y-1)*(y-2)
        testPoints = [[0,0],[0,1],[0,2],[1,3],[1,4],[1,5]]
        for point in testPoints:
          xVal = point[0]
          yVal = point[1]
          actualValue = f_actual.evaluate(xVal,yVal)
          expectedValue = f_expected.evaluate(xVal,yVal)
          tol = 1e-12
          if abs(actualValue-expectedValue) > tol :
            print "At (" + str(xVal) + "," + str(yVal) + "), expected ",
            print str(expectedValue) + ", but value was " + str(actualValue)
          self.assertAlmostEqual(f_actual.evaluate(xVal,yVal), f_expected.evaluate(xVal,yVal), delta=1e-12)

    def testBasicRoberts2(self):
        mySolver = Solver(True)
        f_actual = mySolver.functionParser("3*(1-y)*(y-2)")
        y = Function.yn(1)
        f_expected = -3*(y-1)*(y-2)
        testPoints = [[0,0],[0,1],[0,2],[1,3],[1,4],[1,5]]
        for point in testPoints:
          xVal = point[0]
          yVal = point[1]
          self.assertAlmostEqual(f_actual.evaluate(xVal,yVal), f_expected.evaluate(xVal,yVal), delta=1e-12)

    def testBasicRoberts3(self):
        mySolver = Solver(True)
        f_actual = mySolver.functionParser("-3*y*y+9*y-6")
        y = Function.yn(1)
        f_expected = -3*(y-1)*(y-2)
        testPoints = [[0,0],[0,1],[0,2],[1,3],[1,4],[1,5]]
        for point in testPoints:
          xVal = point[0]
          yVal = point[1]
          self.assertAlmostEqual(f_actual.evaluate(xVal,yVal), f_expected.evaluate(xVal,yVal), delta=1e-12)

    def testNestedParen(self):
        x = Solver(True)
        y = x.functionParser("4*((x+1)+(x*2))")
        z = 4 * ((Function.xn(1) + 1) + (Function.xn(1) * 2))
        self.assertAlmostEqual(z.evaluate(2,2), y.evaluate(2,2), delta=1e-12)

    def testExponent(self):
        x = Solver(True)
        y = x.functionParser("x^2")
        z = Function.xn(2)
        self.assertAlmostEqual(z.evaluate(2,2), y.evaluate(2,2), delta=1e-12)


if (__name__ == '__main__'):
  unittest.main()
