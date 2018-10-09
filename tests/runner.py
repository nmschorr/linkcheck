import unittest
from tests import test_one
from tests import test_two



class suitetests(unittest.TestCase):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTest(suite.addTests(loader.loadTestsFromModule(test_one)))
    suite.addTest(suite.addTests(loader.loadTestsFromModule(test_two)))
    #runner = unittest.TextTestRunner(verbosity=2)
    #print(runner.run(suite))
    unittest.TextTestRunner(verbosity=2).run(suite)

suitetests()
## unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
     unittest.main()

     #verbosity=2