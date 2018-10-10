import unittest
from linkcheck import LinkCheckLib as lclib

class test_two(unittest.TestCase):


    def setUp(self):
        """ Setting up for the test """
        self.lcb = lclib()
        print("\n")
        print("----------------In setUp - CLASS: test_two")
        print("Running test: ", self._testMethodName)


    def test_link3(self):
        test_name = "test_link3"
        test_link = "one.html"
        exp_link = "http://one.html"

        ans = self.lcb.ckaddymore(test_link)
        self.assertEquals(ans, exp_link)

    def test_link4(self):
        test_name = "test_link4"
        test_link = "http://one.html"
        exp_link = "http://one.html"

        ans = self.lcb.ckaddymore(test_link)
        self.assertEquals(ans, exp_link)

    def test_link5(self):
        test_name = "test_link5"
        test_link = "https://one.html"
        exp_link = "https://one.html"

        ans = self.lcb.ckaddymore(test_link)
        self.assertEquals(ans, exp_link)

    def test_link6(self):
        test_name = "test_link6"
        test_link6 = "http//one.html"
        exp_link = "https://one.html"

        ans = self.lcb.ckaddymore(test_link6)
        self.assertEquals(ans, exp_link)

    def test_link7(self):
        test_name = "test_link7"
        test_link7 = "http//one.html"
        exp_link = "https://one.html"

        ans = self.lcb.ckaddymore(test_link7)
        self.assertEquals(ans, exp_link)

    def test_link8(self):
        test_name = "test_link8"
        test_link8 = "http//onebigurlstring#.html"
        exp_link = "https://one.html"

        ans, ans2 = self.lcb.ck_bad_data(test_link8)
        self.assertEquals(ans, 1)
        self.assertTrue(ans2)

    def test_link9(self):
        test_name = "test_link9"
        test_link9 = "http//onebigurlstring.html"

        ans, ans2 = self.lcb.ck_bad_data(test_link9)
        self.assertEquals(ans, 0)
        self.assertTrue(ans2)

    def test_link10(self):
        test_name = "test_link6"
        test_link6 = "http//onebigurlstring.fff"

        ans, ans2 = self.lcb.ck_bad_data(test_link6)
        self.assertEquals(ans, 0)
        self.assertFalse(ans2)

    def test_link11(self):
        test_name = "test_link11"
        test_link11 = "http//onebigurlstring.fff"  #bad

        ans, ans2 = self.lcb.ck_bad_data(test_link11)
        self.assertEquals(ans, 0)
        self.assertFalse(ans2)

    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        print("Done with test: ", self._testMethodName, " --RESULT: ")





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
