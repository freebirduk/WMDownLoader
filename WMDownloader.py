import configparser
import os
import sys
import winsound

from DateTimeProvider import DateTimeProvider
from MainRoutine import MainRoutine
from WeatherUndergroundApiService import WeatherUndergroundApiService
from WMDatabaseService import WMDatabaseService
from WMErrorService import WMErrorService

# Launches the Weather Manager Downloader

# Get configuration
_config = configparser.ConfigParser()
_config.read('config.ini')
if _config is None:
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    print(f"Could not read the configuration file config.ini in {os.getcwd()}")
    input("Press return to continue")
    sys.exit()

# Instance the services for WU Api, database, date and errors

error_service = WMErrorService(_config.get("EMail", "Host"),
                               _config.get("EMail", "Port"),
                               _config.get("EMail", "Username"),
                               _config.get("EMail", "Password"),
                               _config.get("EMail", "FromAddress"),
                               _config.get("EMail", "FromName"),
                               _config.get("EMail", "ToAddress"),
                               _config.get("EMail", "ToName"))

database_service = WMDatabaseService(_config.get("Database", "IPAddress"),
                                     _config.get("Database", "Port"),
                                     _config.get("Database", "UserId"),
                                     _config.get("Database", "Password"),
                                     _config.get("Database", "DatabaseName"),
                                     error_service)

date_time_provider = DateTimeProvider()

wu_underground_api_service = WeatherUndergroundApiService(_config.get("WeatherUnderground", "StationId"),
                                                          _config.get("WeatherUnderground", "ApiKey"))

# Instance the MainRoutine injecting these services.

main_routine = MainRoutine(database_service,
                           date_time_provider,
                           WeatherUndergroundApiService,
                           error_service,
                           _config.get("Downloader", "ApiThrottlingLimit"),
                           _config.get("WeatherUnderground", "InitialObservationDate"),
                           _config.get("Downloader", "LogFile"))

# Run the MainRoutine
main_routine.download_recent_observations()
