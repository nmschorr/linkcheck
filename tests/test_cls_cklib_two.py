import unittest
# from linkcheck import LinkCheckLib as lclib
import linkchecklib

class TestCls_cklib_two(unittest.TestCase):

    # def setUpClass(cls):
    #     print("----------------In setUpClass: TestCls_cklib_two ")
    #     print("----------------")

    def setUp(self):
        """ Setting up for the test """
        self.lcb = linkchecklib.LinkCheckLib()
        print("\n")
        print("----------------In setUp - CLASS: TestCls_cklib_two")
        print("Running test: ", self._testMethodName)
        self.BASENAME = self.lcb.BASENAME
        self.BASENAMEwww = self.lcb.BASENAMEwww
        self.lcb.MAIN_DICT.update({self.BASENAME: "mockname.com"})
        self.lcb.MAIN_DICT.update({self.BASENAMEwww: "www.mockname.com"})
        self.lcb.MAIN_DICT.update({self.lcb.rbase: "mockname.com"})
        #self.base_lnks_g = self.MAIN_DICT.get(self.rbase)

    # ----------------------------------------------------mk_link_w_scheme
    def test_cklib_two1(self):
        test_link = "one.html"
        exp_link = "http://one.html"
        ans = self.lcb.mk_link_w_scheme(test_link)
        self.assertEquals(ans, exp_link)

    def test_cklib_two2(self):
        test_link = "http://one.html"
        exp_link = "http://one.html"
        ans = self.lcb.mk_link_w_scheme(test_link)
        self.assertEquals(ans, exp_link)


    def test_cklib_two3(self):
        test_link = "https://one.html"
        exp_link = "https://one.html"
        ans = self.lcb.mk_link_w_scheme(test_link)
        self.assertEquals(ans, exp_link)

        # ----------------------------------------------------make_www_url

    def test_cklib_two4(self):
        test_link = "one.html"
        exp_link = "www.one.html"
        ans = self.lcb.make_www_url(test_link)
        self.assertEquals(ans, exp_link)


    def test_cklib_two5(self):
        test_link = "https://one.html"
        exp_link = "https://www.one.html"
        ans = self.lcb.make_www_url(test_link)
        self.assertNotEqual(ans, exp_link)

    def test_cklib_two6(self):
        test_link6 = "http//one.html"
        exp_link = "http://www.one.html"
        ans = self.lcb.make_www_url(test_link6)
        self.assertNotEqual(ans, exp_link)


        # ----------------------------------------------------ck_bad_data

    def test_cklib_two7(self):
        test_link7 = "http//one.html"
        exp_link = "https://one.html"
        ans = self.lcb.ck_bad_data(test_link7)
        self.assertNotEqual(ans, exp_link)

    def test_cklib_two8(self):
        test_link8 = "http//onebigurlstring#.html"
        exp_link = "https://one.html"
        ans, ans2 = self.lcb.ck_bad_data(test_link8)
        self.assertEquals(ans, 1)
        self.assertTrue(ans2)

    def test_cklib_two9(self):
        test_link9 = "http://onebigurlstring+more.html"
        ans, ans2 = self.lcb.ck_bad_data(test_link9)
        self.assertEquals(ans, 0)
        self.assertTrue(ans2)

        # ----------------------------------------------------isTHEparent


    def test_cklib_two10(self):
        test_link10 = "http//onebigurlstring.fff"
        ans = self.lcb.isTHEparent(test_link10)
        self.assertFalse(ans)

    def test_cklib_two11(self):
        test_link11 = "mockname"
        ans = self.lcb.isTHEparent(test_link11)
        self.assertTrue(ans)

    def test_cklib_two12(self):
        test_link12 = "www.mockname"
        ans = self.lcb.isTHEparent(test_link12)
        self.assertTrue(ans)

    # ----------------------------------------------------ret_bool_if_BASE

    def test_cklib_two13(self):
        test_link13 = "http//onebigurlstring.fff"
        ans = self.lcb.ret_bool_if_BASE(test_link13)
        self.assertFalse(ans)

    def test_cklib_two14(self):
        test_link14 = "mockname"
        ans = self.lcb.ret_bool_if_BASE(test_link14)
        self.assertTrue(ans)

    def test_cklib_two15(self):
        test_link15 = "www.mockname"
        ans = self.lcb.ret_bool_if_BASE(test_link15)
        self.assertTrue(ans)

        # ----------------------------------------------------ret_bool_if_in_BASE_glob

    def test_cklib_two15(self):
        test_link15 = "mockname.com"
        ans = self.lcb.ret_bool_if_in_BASE_glob(test_link15)
        self.assertTrue(ans)

        # ----------------------------------------------------ret_bool_if_in_BASE_glob

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
