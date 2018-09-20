import unittest
from tests import test_one

## unittest.TextTestRunner(verbosity=2).run(suite)


class suitetests(unittest.TestCase):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(test_one.TestCaseLC))
    runner = unittest.TextTestRunner(verbosity=2)
    print(runner.run(suite))

suitetests()

if __name__ == '__main__':
     unittest.main()