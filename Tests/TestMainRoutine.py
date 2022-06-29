import configparser
from DateTimeProvider import DateTimeProvider
from MainRoutine import MainRoutine
from unittest import TestCase
from WMDatabaseService import WMDatabaseService
from WeatherUndergroundApiService import WeatherUndergroundApiService


class TestMainRoutine(TestCase):
    config = configparser.ConfigParser()

    def setUp(self):
        self.config.read('config.ini')

    def test_download_recent_observations_live_data(self):

        _wm_database_service = WMDatabaseService(self.config.get('Database', 'IPAddress'),
                                                 self.config.get('Database', 'Port'),
                                                 self.config.get('Database', 'UserId'),
                                                 self.config.get('Database', 'Password'),
                                                 self.config.get('Database', 'DatabaseName'))

        _date_time_provider = DateTimeProvider

        _wu_api_service = WeatherUndergroundApiService(self.config.get('WeatherUnderground', 'StationId'),
                                                       self.config.get('WeatherUnderground', 'ApiKey'))

        main_routine = MainRoutine(_wm_database_service, _date_time_provider, _wu_api_service)

        _success = main_routine.download_recent_observations()

        self.assertTrue(_success)
