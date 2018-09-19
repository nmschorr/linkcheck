import unittest
#from unittest import *
from linkchecklib import LinkCheckLib
from linkcheck import LinkCheck



class MyTestCase(unittest.TestCase):
    test_link = "schorrmedbbbbbbb"


    def test_something(test_link):
        lctest = LinkCheckLib()
        finans = lctest.has_correct_suffix(test_link)
        unittest.TestCase.assertFalse(lctest.has_correct_suffix(test_link))


if __name__ == '__main__':
    unittest.main()
