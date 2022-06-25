import configparser
import os
import unittest
from datetime import datetime
from datetime import date
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

        _initial_observation_date = datetime.strptime(self.config.get('WeatherUnderground',
                                                                      'InitialObservationDate'),
                                                      '%Y-%m-%d')

        result = service.get_most_recent_observation_date(_initial_observation_date.date())
        self.assertEqual(result, date(2022, 6, 6))

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

        _initial_observation_date = datetime.strptime(self.config.get('WeatherUnderground',
                                                                      'InitialObservationDate'),
                                                      '%Y-%m-%d')

        result = service.get_most_recent_observation_date(_initial_observation_date.date())
        self.assertEqual(result, _initial_observation_date.date())

        service.dispose()


if __name__ == '__main__':
    unittest.main()
