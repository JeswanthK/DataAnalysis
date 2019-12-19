import unittest
import mock
import source.alerts.send_email as send_email
import common.path_to_use as paths
import sys

sys.path.append('../')



class test_get_functions(unittest.TestCase):

    @mock.patch('paths.getEmail()', return_value='FCAEmail')
    def test_get_email(self):
        self.assertEqual(send_email.get_email(), 'FCAEmail')

    @mock.patch('paths.getEmailPassword()', return_value='FCAPassword')
    def test_get_email_password(self):
        self.assertEqual(send_email.get_email_password(), 'FCAPassword')

    def test_get_message(self):
        self.assertEqual(send_email.get_message(), 'xd')


suite = unittest.TestSuite()
suite.addTest(test_get_functions)
unittest.TextTestRunner().run(suite)
