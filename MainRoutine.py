# Main logic for importing Weather Underground PWS data and adding it to the Weather Manager database.
# Will import all observations not yet downloaded up until yesterday's date.

import configparser
import IWMDatabaseService
import IWeatherUndergroundApiService


class MainRoutine:
    config = configparser.ConfigParser()
    database_service = None
    wu_service = None

    def __init__(self,
                 wm_database_service: IWMDatabaseService,
                 wu_api_service: IWeatherUndergroundApiService):

        self.config.read('config.ini')

        self.database_service = wm_database_service
        self.wu_service = wu_api_service

    def download_recent_observations(self):

        # Weather Underground not recording today warner

        most_recent_observation_date = \
            self.database_service.get_most_recent_observation_date(self.config.get('WeatherUnderground',
                                                                                   'InitialObservationDate'))

        # Fetch the latest observations

        # Save the latest observations
