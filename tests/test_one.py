import unittest
from linkcheck import LinkCheckLib as lclib

class TestCaseLC(unittest.TestCase):
    def __init__(self):
        super().__init__()
        lcb = lclib()
        self.lcb = lcb

    def setUp(self):
        """ Setting up for the test """
        print("setUp_:begin")
        intro = "Testname is: "
        testName = self.shortDescription()
        if len(testName) > 0:
            print(intro + testName)
        else:
            print("UNKNOWN TEST ROUTINE")
        print("setUp_:end")

    def test_link1(self):
        test_link = "schorrmedbbbbbbb"
        self.assertFalse(self.lcb.check_sufx(test_link))

    def test_link2(self):
        test_link = "schorrmedbbbb.com"
        #self.assertTrue('FOO'.isupper())
        self.assertTrue(self.lcb.check_sufx(test_link))


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
