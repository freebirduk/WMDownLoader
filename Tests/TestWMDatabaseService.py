import configparser
import datetime
import os
import unittest
from unittest import TestCase
from Tests.MaintainTestDatabase import MaintainTestDatabase
from WMDatabaseService import WMDatabaseService


class TestWMDatabaseService(TestCase):
    config = configparser.ConfigParser()
    directory_path = os.getcwd() + "\\Tests\\"

    def setUp(self):
        self.config.read('config.ini')

    # A most recent observation date gets successfully retrieved
    def test_get_most_recent_observation_date_successful(self):
        maintain_database = MaintainTestDatabase(self.config)
        maintain_database.load_test_database(self.directory_path + "GetMostRecentObservation.json")

        # noinspection DuplicatedCode
        service = WMDatabaseService(self.config.get('Database', 'IPAddress'),
                                    self.config.get('Database', 'Port'),
                                    self.config.get('Database', 'UserId'),
                                    self.config.get('Database', 'Password'),
                                    self.config.get('Database', 'DatabaseName'))

        result = service.get_most_recent_observation_date(self.config.get('WeatherUnderground',
                                                                          'InitialObservationDate'))
        self.assertEqual(result, datetime.datetime(2022, 6, 6, 22, 9, 57))

        service.dispose()

    # The database is empty so no most recent observation date can be retrieved
    def test_get_most_recent_observation_date_none_there(self):
        maintain_database = MaintainTestDatabase(self.config)
        maintain_database.load_test_database(None)

        # noinspection DuplicatedCode
        service = WMDatabaseService(self.config.get('Database', 'IPAddress'),
                                    self.config.get('Database', 'Port'),
                                    self.config.get('Database', 'UserId'),
                                    self.config.get('Database', 'Password'),
                                    self.config.get('Database', 'DatabaseName'))

        result = service.get_most_recent_observation_date(self.config.get('WeatherUnderground',
                                                                          'InitialObservationDate'))
        self.assertEqual(result, self.config.get('WeatherUnderground', 'InitialObservationDate'))

        service.dispose()


if __name__ == '__main__':
    unittest.main()
