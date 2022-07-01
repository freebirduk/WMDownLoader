import configparser
from datetime import date
from unittest import TestCase
from WeatherUndergroundApiService import WeatherUndergroundApiService


class TestWeatherUndergroundApiServiceLive(TestCase):
    config = configparser.ConfigParser()

    def setUp(self):
        self.config.read('config.ini')

    def test_get_hourly_observations_for_date(self):
        _service = WeatherUndergroundApiService(self.config.get('WeatherUnderground', 'StationId'),
                                                self.config.get('WeatherUnderground', 'ApiKey'))

        _service.start_wu_api_session()
        results = _service.get_hourly_observations_for_date(date(2021, 7, 20))
        _service.stop_wu_api_session()
        self.assertEqual(len(results["observations"]), 24)

    def test_missing_station_id(self):
        with self.assertRaises(Exception) as context:
            _service = WeatherUndergroundApiService("", self.config.get('WeatherUnderground', 'ApiKey'))
        self.assertTrue("Station Id not provided to Weather Underground API service" in str(context.exception))

    def test_missing_api_key(self):
        with self.assertRaises(Exception) as context:
            _service = WeatherUndergroundApiService(self.config.get('WeatherUnderground', 'StationId'), "")
        self.assertTrue("API Key not provided to Weather Underground API service" in str(context.exception))

    def test_wrong_api_key(self):
        _service = WeatherUndergroundApiService(self.config.get('WeatherUnderground', 'StationId'),
                                                "bad key test")
        with self.assertRaises(Exception) as context:
            _service.start_wu_api_session()
            _service.get_hourly_observations_for_date(date(2021, 7, 20))
            _service.stop_wu_api_session()
        self.assertTrue("Weather Underground API returned 401 'Unauthorized'" in str(context.exception))
