import unittest
from linkcheck import LinkCheckLib as lcc

class TestCaseLC2(unittest.TestCase):
    lcobj = lcc()

    def test_link3(self):
        test_link = "one.html"
        exp_link = "http://one.html"

        ans = lcc.ckaddymore(test_link)
        self.assertEquals(ans, exp_link)

    def test_link4(self):
        test_link = "http://one.html"
        exp_link = "http://one.html"

        ans = lcc.ckaddymore(test_link)
        self.assertEquals(ans, exp_link)

    def test_link5(self):
        test_link = "https://one.html"
        exp_link = "https://one.html"

        ans = lcc.ckaddymore(test_link)
        self.assertEquals(ans, exp_link)

    def test_link6(self):
        test_link = "http//one.html"
        exp_link = "https://one.html"

        ans = lcc.ckaddymore(test_link)
        self.assertEquals(ans, exp_link)

    def test_link7(self):
        test_link = "http//one.html"
        exp_link = "https://one.html"

        ans = lcc.ckaddymore(test_link)
        self.assertEquals(ans, exp_link)

    def test_link8(self):
        test_link = "http//onebigurlstring#.html"
        exp_link = "https://one.html"

        ans, ans2 = lcc.ck_bad_data(test_link)
        self.assertEquals(ans, 1)
        self.assertTrue(ans2)

    def test_link9(self):
        test_link = "http//onebigurlstring.html"

        ans, ans2 = lcc.ck_bad_data(test_link)
        self.assertEquals(ans, 0)
        self.assertTrue(ans2)

    def test_link10(self):
        test_link = "http//onebigurlstring.fff"

        ans, ans2 = lcc.ck_bad_data(test_link)
        self.assertEquals(ans, 0)
        self.assertFalse(ans2)

    def test_link10(self):
        test_link = "http//onebigurlstring.fff"  #bad

        ans, ans2 = lcc.ck_bad_data(test_link)
        self.assertEquals(ans, 0)
        self.assertFalse(ans2)


# ck_bad_data(self, dlink):





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
