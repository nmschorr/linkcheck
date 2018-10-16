import unittest
from tests import test_cls_cklib_one, test_cls_cklib_two
import sys

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_cls_cklib_one))
suite.addTests(loader.loadTestsFromModule(test_cls_cklib_two))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(stream=sys.stdout,verbosity=2)
#runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

unittest.TextTestRunner
