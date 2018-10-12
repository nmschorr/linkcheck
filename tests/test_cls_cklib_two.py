import unittest
from linkcheck import LinkCheckLib as lclib

class TestCls_cklib_two(unittest.TestCase):

    # def setUpClass(cls):
    #     print("----------------In setUpClass: TestCls_cklib_two ")
    #     print("----------------")

    def setUp(self):
        """ Setting up for the test """
        self.lcb = lclib()
        print("\n")
        print("----------------In setUp - CLASS: TestCls_cklib_one")
        print("Running test: ", self._testMethodName)

    # ----------------------------------------------------ckaddymore
    def test_cklib_two1(self):
        test_link = "one.html"
        exp_link = "http://one.html"

        ans = self.lcb.mk_link_w_scheme(test_link)
        self.assertEquals(ans, exp_link)

    def test_cklib_two2(self):
        test_link = "one.html"
        exp_link = "http://one.html"

        ans = self.lcb.mk_link_w_scheme(test_link)
        self.assertEquals(ans, exp_link)


    def test_cklib_two3(self):
        test_link = "one.html"
        exp_link = "http://one.html"

        ans = self.lcb.mk_link_w_scheme(test_link)
        self.assertEquals(ans, exp_link)

    def test_cklib_two4(self):
        test_link = "http://one.html"
        exp_link = "http://one.html"

        ans = self.lcb.mk_link_w_scheme(test_link)
        self.assertEquals(ans, exp_link)

    def test_cklib_two5(self):
        test_link = "https://one.html"
        exp_link = "https://one.html"

        ans = self.lcb.mk_link_w_scheme(test_link)
        self.assertEquals(ans, exp_link)

    def test_cklib_two6(self):
        test_link6 = "http//one.html"
        exp_link = "https://one.html"

        ans = self.lcb.mk_link_w_scheme(test_link6)
        self.assertEquals(ans, exp_link)

    def test_cklib_two7(self):
        test_link7 = "http//one.html"
        exp_link = "https://one.html"

        ans = self.lcb.mk_link_w_scheme(test_link7)
        self.assertEquals(ans, exp_link)

    def test_cklib_two8(self):
        test_link8 = "http//onebigurlstring#.html"
        exp_link = "https://one.html"

        # ----------------------------------------------------ck_bad_data
        ans, ans2 = self.lcb.ck_bad_data(test_link8)
        self.assertEquals(ans, 1)
        self.assertTrue(ans2)

    def test_cklib_two9(self):
        test_link9 = "http//onebigurlstring.html"

        ans, ans2 = self.lcb.ck_bad_data(test_link9)
        self.assertEquals(ans, 0)
        self.assertTrue(ans2)

    def test_cklib_two10(self):
        test_link6 = "http//onebigurlstring.fff"

        ans, ans2 = self.lcb.ck_bad_data(test_link6)
        self.assertEquals(ans, 0)
        self.assertFalse(ans2)

    def test_cklib_two11(self):
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
