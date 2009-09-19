import unittest
import doctest

if __name__=="__main__":
    suite = doctest.DocFileSuite('README.txt')
    runner = unittest.TextTestRunner()
    runner.run(suite)
