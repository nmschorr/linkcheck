import unittest
from linkcheck import LinkCheckLib as lclib
import sys

class test_one(unittest.TestCase):

    def setUp(self):
        """ Setting up for the test """
        self.lcb = lclib()
        print("\n")
        print("----------------In setUp - CLASS: test_one")
        print("Running test: ", self._testMethodName)

    def test_link1(self):
        test_name = self._testMethodName
        test_link = "schorrmedbbbbbbb"
        self.assertFalse(self.lcb.check_sufx(test_link))

    def test_link2(self):
        test_name = self._testMethodName
        test_link = "schorrmedbbbb.com"
        self.assertTrue(self.lcb.check_sufx(test_link))

    def tearDown(self):
        """Cleaning up after the test"""
        print("Done with test: ", self._testMethodName, " --RESULT: ")








#
#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')
#
#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())
#
#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)
