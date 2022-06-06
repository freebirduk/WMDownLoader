import datetime
from unittest import TestCase
from WMDatabaseService import WMDatabaseService
import configparser


class TestWMDatabaseService(TestCase):
    config = configparser.ConfigParser()
    service = None

    def setUp(self):
        self.config.read('config.ini')
        self.service = WMDatabaseService(self.config.get('Database', 'IPAddress'),
                                         self.config.get('Database', 'Port'),
                                         self.config.get('Database', 'UserId'),
                                         self.config.get('Database', 'Password'),
                                         self.config.get('Database', 'DatabaseName'))

    def test_get_most_recent_observation_date(self):
        result = self.service.get_most_recent_observation_date()
        self.assertEqual(result, datetime.datetime(2022, 6, 6, 22, 9, 57))
