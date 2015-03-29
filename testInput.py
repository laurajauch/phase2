import subprocess
import unittest

# method to open the specified input file
def testFile(filename):
    cmd = "python main.py".split()
    with open(filename, "r") as input:
        subprocess.call(cmd, stdin=input)

class testInput(unittest.TestCase):

    # Template for writing tests in this class
    def testTest(self):
        # Name of the file with the input strings for this test
        testFile("inputStrings")
        # Unsure of what we'd assert
