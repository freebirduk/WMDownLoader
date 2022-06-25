# Main logic for importing Weather Underground PWS data and adding it to the Weather Manager database.
# Will import all observations not yet downloaded up until yesterday's date.

import configparser
import IDateTimeProvider
import IWMDatabaseService
import IWeatherUndergroundApiService
from datetime import date
from datetime import datetime
from datetime import timedelta


class MainRoutine:
    _config = configparser.ConfigParser()
    _database_service = None
    _date_time_provider = None
    _wu_service: IWeatherUndergroundApiService = None

    def __init__(self,
                 wm_database_service: IWMDatabaseService,
                 date_time_provider: IDateTimeProvider,
                 wu_api_service: IWeatherUndergroundApiService):

        self._config.read('config.ini')

        self._database_service = wm_database_service
        self._date_time_provider = date_time_provider
        self._wu_service = wu_api_service

    # The controlling method that is called to drive the download of recent observations
    def download_recent_observations(self):

        # Weather Underground not recording today warner

        _initial_observation_date = datetime.strptime(self._config.get('WeatherUnderground',
                                                                       'InitialObservationDate'),
                                                      '%Y-%m-%d').date()
        _most_recent_observation_date: date = \
            self._database_service.get_most_recent_observation_date(_initial_observation_date)

        _fetch_up_to_date = self._apply_api_throttling_limit(self._date_time_provider.now(self) -
                                                             timedelta(days=1),
                                                             _most_recent_observation_date)

        _retrieved_observations = self._retrieve_recent_observations(_most_recent_observation_date,
                                                                     _fetch_up_to_date)

        self._database_service.save_list_of_observations(_retrieved_observations)

        return True

    # To avoid tripping the Weather Underground API throttling limit this will restrict the number of
    # recent observations downloaded to the value set in the config file. Outstanding observations will
    # get downloaded on subsequent days.
    def _apply_api_throttling_limit(self, yesterdays_date: date, most_recent_observation_date: date):

        _api_throttle_limit: timedelta = timedelta(days=float(self._config.get('Downloader',
                                                                               'ApiThrottlingLimit')))

        if yesterdays_date - most_recent_observation_date > _api_throttle_limit:
            return most_recent_observation_date + _api_throttle_limit
        else:
            return yesterdays_date

    # Repeatedly call the Weather Underground API to obtain recent observations
    def _retrieve_recent_observations(self, most_recent_observation_date: date, fetch_up_to_date: date):

        _observation_list = []

        _date_counter: date = most_recent_observation_date + timedelta(days=1)

        while _date_counter <= fetch_up_to_date:

            _retrieved_observation = self._wu_service.get_hourly_observations_for_date(_date_counter)

            if _retrieved_observation is not None:
                _observation_list.append(_retrieved_observation)

            _date_counter = _date_counter + timedelta(days=1)

        return _observation_list

