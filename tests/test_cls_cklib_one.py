import unittest
from linkcheck import LinkCheckLib as lclib
# LinkCheckLib: tests check_sufx, ck_bad_data, ckaddymore

class TestCls_cklib_one(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     print("----------------In setUpClass------------")


    def setUp(self): # Setting up for the test
        self.lcb = lclib()
        print("---------> ", self._testMethodName, " ------->")

    # ----------------------------------------------------check_sufx

    def test_link1(self):
        #test_name = "-------" + self._testMethodName
        test_link = "appleorangelemon"
        self.assertFalse(self.lcb.ck_tld_sufx(test_link))

    def test_link1b(self):
        # test_name = "-------" + self._testMethodName
        test_link = "appleorang.freakyelemon"
        self.assertFalse(self.lcb.ck_tld_sufx(test_link))

    def test_link1b(self):
        # test_name = "-------" + self._testMethodName
        test_link = "appleorang.etphonehome/"
        self.assertFalse(self.lcb.ck_tld_sufx(test_link))

    def test_link2(self):
        test_link = "orangelemon.gov"
        self.assertTrue(self.lcb.ck_tld_sufx(test_link))

    def test_link2b(self):
        test_link = "happycamper.com/"
        self.assertTrue(self.lcb.ck_tld_sufx(test_link))

    def test_link2c(self):
        test_link = "face.au/"
        self.assertTrue(self.lcb.ck_tld_sufx(test_link))

    #----------------------------------------------------ck_bad_data
    def test_link3(self):
        test_link = "facebook.com"
        first_int, sec_ans = self.lcb.ck_bad_data(test_link)
        self.assertTrue(first_int > 0)  ## over 0 if it's bad
        self.assertTrue(sec_ans)

    def test_link4(self):
        test_link = 'facebooktel:+'
        first_int, sec_ans = self.lcb.ck_bad_data(test_link)
        self.assertTrue(first_int > 0)  ## over 0 if it's bad
        self.assertFalse(sec_ans)

    def test_link5(self):
        test_link = "ccccccccschorr#"
        first_int, sec_ans = self.lcb.ck_bad_data(test_link)
        self.assertTrue(first_int > 0)  ## over 0 if it's bad
        self.assertFalse(sec_ans)

    def test_link6(self):
        test_link = "schorrmedbbbb.com#twitter.com"
        first_int, sec_ans = self.lcb.ck_bad_data(test_link)
        self.assertTrue(first_int > 0)  ## over 0 if it's bad
        self.assertTrue(sec_ans)
    # ----------------------------------------------------ckaddymore

    def test_link7(self):
        test_link = 'http://abcd.com'
        tanswer = self.lcb.ckaddymore(test_link)
        right_answer = 'http://abcd.com'
        self.assertEquals(self.lcb.ckaddymore(tanswer), right_answer)

    def test_link8(self):
        test_link = 'https://abcd.com'
        right_answer = 'https://abcd.com'
        self.assertEquals(self.lcb.ckaddymore(test_link), right_answer)

    def test_link9(self):
        test_link = 'http://abcdesomethingelse.xxx.com'
        right_answer =  'http://abcdesomethingelse.xxx.com'
        self.assertEquals(self.lcb.ckaddymore(test_link), right_answer)

    def test_link10(self):
        test_link = 'abcdesomethingelse.xxx.com'
        right_answer = 'http://abcdesomethingelse.xxx.com'
        self.assertEquals(self.lcb.ckaddymore(test_link), right_answer)

    def test_link11(self):
        test_link = 'abcdg.com'
        right_answer = 'http://abcdg.com'
        self.assertEquals(self.lcb.ckaddymore(test_link), right_answer)
    # ----------------------------------------------------x



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
