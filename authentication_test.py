import unittest
import sys
import authentication_utils as au

class TestAuthenticationUtilities(unittest.TestCase):
    def test_account_exists(self):
        self.assertTrue(au.account_exists('t_username'))
    
    def test_fetch_id(self):
        self.assertEqual(au.fetch_id('t_username'), 1)

    def test_password_valid(self):
        self.assertTrue(au.password_valid(1, 't_password'))

    def test_account_number_exists(self):
        self.assertTrue(au.account_number_exists('0000000000'))

loader = unittest.TestLoader()
suite = loader.loadTestsFromTestCase(TestAuthenticationUtilities)
runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
runner.run(suite)
