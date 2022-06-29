import configparser
from WMEmailService import WMEmailService
from unittest import TestCase


class TestWMEmailService(TestCase):
    config = configparser.ConfigParser()

    def setUp(self):
        self.config.read('config.ini')

    def test_send_email(self):

        _wm_email_service = WMEmailService(self.config.get('EMail', 'Host'),
                                           self.config.get('EMail', 'Port'),
                                           self.config.get('EMail', 'Username'),
                                           self.config.get('EMail', 'Password'),
                                           self.config.get('EMail', 'FromAddress'),
                                           self.config.get('EMail', 'FromName'),
                                           self.config.get('EMail', 'ToAddress'),
                                           self.config.get('EMail', 'ToName'))

        _success = _wm_email_service.send_email("Test message")

        self.assertTrue(_success)
