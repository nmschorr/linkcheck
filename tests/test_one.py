import unittest
from linkcheck import LinkCheckLib

class TestCaseLC(unittest.TestCase):

    def test_link1(self):
        test_link = "schorrmedbbbbbbb"
        lctest = LinkCheckLib()
        self.assertFalse(lctest.check_sufx(test_link))

    def test_link2(self):
        test_link = "schorrmedbbbb.com"
        lctest = LinkCheckLib()
        #self.assertTrue('FOO'.isupper())
        self.assertTrue(lctest.check_sufx(test_link))


if __name__ == '__main__':
    unittest.main()




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
