import unittest
from tests import test_one
from tests import test_two





class suitetests(unittest.TestCase):

    def __init__(self):

        loader = unittest.TestLoader()
        self.loader = loader
    #suite = unittest.TestSuite()

    # suite.addTest(suite.addTests(loader.loadTestsFromModule(test_one)))
    # suite.addTest(suite.addTests(loader.loadTestsFromModule(test_two)))
    #runner = unittest.TextTestRunner(verbosity=2)
    #print(runner.run(suite))
    #unittest.TextTestRunner(verbosity=2).run(suite)

    def make_suite(self):
        msuite = unittest.TestSuite()
        # suite.addTest(WidgetTestCase('test_default_widget_size'))
        # suite.addTest(WidgetTestCase('test_widget_resize'))
        msuite.addTest(msuite.addTests(self.loader.loadTestsFromModule(test_one)))
        msuite.addTest(msuite.addTests(self.loader.loadTestsFromModule(test_two)))
        return msuite


if __name__ == '__main__':
    stests = suitetests()
    runner = unittest.TextTestRunner()
    runner.run(stests)  ## unittest.TextTestRunner(verbosity=2).run(suite)

    #verbosity=2