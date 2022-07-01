# Main logic for importing Weather Underground PWS data and adding it to the Weather Manager database.
# Will import all observations not yet downloaded up until yesterday's date.

import configparser
import IDateTimeProvider
import IWMDatabaseService
import IWMErrorService
import IWeatherUndergroundApiService
import logging
import os
import sys
from datetime import date
from datetime import datetime
from datetime import timedelta
from os.path import exists

import WuApiException


def _configure_logging(log_file_full_name: str):
    _log_format = "%(asctime)s - %(levelname)s - %(message)s"

    if exists(log_file_full_name):
        logging.basicConfig(filename=log_file_full_name, format=_log_format)
    else:
        logging.basicConfig(filename="WMDownloader.log", format=_log_format)
        logging.warning(f"Couldn't file the supplied log file {log_file_full_name}")


class MainRoutine:
    _config = configparser.ConfigParser()
    _database_service = None
    _date_time_provider = None
    _wm_error_service = None
    _wu_api_service: IWeatherUndergroundApiService = None

    def __init__(self,
                 wm_database_service: IWMDatabaseService,
                 date_time_provider: IDateTimeProvider,
                 _wu_api_service: IWeatherUndergroundApiService,
                 _wm_error_service: IWMErrorService,
                 log_file_full_name):

        # Setup logging
        _configure_logging(log_file_full_name)

        # Assign function to log unhandled exceptions
        sys.excepthook = self._catch_unhandled_exceptions

        # Load configuration
        self._config.read('config.ini')
        if self._config is None:
            self._wm_error_service.handle_error(f"Could not read the configuration file config.ini in {os.getcwd()}",
                                                "Error", send_email=True, terminate=True)

        # Store the injected services
        self._database_service = wm_database_service
        self._date_time_provider = date_time_provider
        self._wu_service = _wu_api_service
        self._wm_error_service = _wm_error_service

    # The controlling method that is called to drive the download of recent observations
    def download_recent_observations(self):

        self._not_currently_gathering_data_warner()

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

    def _catch_unhandled_exceptions(self, exception_type, value, trace_back):
        if issubclass(exception_type, KeyboardInterrupt):
            sys.__excepthook__(exception_type, value, trace_back)
            return

        self._wm_error_service.handle_error("Critical", "Unhandled exception",
                                            exc_info=(exception_type, value, trace_back))
        sys.exit()

    # Alerts user to the fact that no data has been logged to Weather Underground today.
    # Weather station may be offline for some reason.
    def _not_currently_gathering_data_warner(self):

        try:

            self._wu_service.start_wu_api_sesion()

            _retrieved_observations = self._wu_service.get_hourly_observations_for_date(datetime.now().date())

            if len(_retrieved_observations) == 0:
                self._wm_error_service.handle_error("Weather Underground is not logging observations today",
                                                    "Warning", send_email=True)

            self._wu_service.stop_wu_api_session()

        except WuApiException as ex:

            self._wm_error_service.handle_error(ex, "Critical", send_email=True, terminate=True)

    # Repeatedly call the Weather Underground API to obtain recent observations
    def _retrieve_recent_observations(self, most_recent_observation_date: date, fetch_up_to_date: date):

        _observation_list = []

        _date_counter: date = most_recent_observation_date + timedelta(days=1)

        try:

            self._wu_service.start_wu_api_sesion()

            while _date_counter <= fetch_up_to_date:

                _retrieved_observations = self._wu_service.get_hourly_observations_for_date(_date_counter)

                if _retrieved_observations is not None:
                    _observation_list.append(_retrieved_observations)
                    self._wm_error_service.handle_error(f"No data for {_date_counter} retrieved "
                                                        f"from Weather Underground",
                                                        "Warning")

                _date_counter = _date_counter + timedelta(days=1)

            self._wu_service.stop_wu_api_session()

        except WuApiException as ex:

            self._wm_error_service.handle_error(ex, "Critical", send_email=True, terminate=True)

        return _observation_list
