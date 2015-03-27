from solver import *
from PyCamellia import *
import unittest

class testFunParser(unittest.TestCase):

    def test1(self):
        x = solver(True)
        y = x.functionParser("-3*(y-1)*(y-2)")
        z = -3 * (Function.Function_yn(1)-1)*(Function.Function_yn(1)-2)
        self.assertAlmostEqual(z.evaluate(2,2), y.evaluate(2,2), delta=1e-12)
