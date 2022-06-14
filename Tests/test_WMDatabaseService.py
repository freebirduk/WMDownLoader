import configparser
import datetime
import unittest
from unittest import TestCase
from Tests.MaintainTestDatabase import MaintainTestDatabase
from WMDatabaseService import WMDatabaseService


class TestWMDatabaseService(TestCase):
    config = configparser.ConfigParser()
    database_maintainer = None
    service = None

    def setUp(self):
        self.config.read('config.ini')
        self.service = WMDatabaseService(self.config.get('Database', 'IPAddress'),
                                         self.config.get('Database', 'Port'),
                                         self.config.get('Database', 'UserId'),
                                         self.config.get('Database', 'Password'),
                                         self.config.get('Database', 'DatabaseName'))

        self.database_maintainer = MaintainTestDatabase(self.config)

    def test_get_most_recent_observation_date_successful(self):
        self.database_maintainer.load_test_database("GetMostRecentObservation")
        result = self.service.get_most_recent_observation_date()
        self.assertEqual(result, datetime.datetime(2022, 6, 6, 22, 9, 57))

    def test_get_most_recent_observation_date_none_there(self):
        self.database_maintainer.load_test_database(None)
        result = self.service.get_most_recent_observation_date()
        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
