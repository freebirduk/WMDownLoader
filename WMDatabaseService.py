import logging
import sys

import sqlalchemy.orm
from datetime import date
from datetime import datetime
from IWMDatabaseService import IWMDatabaseService
from sqlalchemy import create_engine, func
from sqlalchemy import exc
from sqlalchemy.ext.automap import automap_base


# Service to handle all interactions with the Weather Manager database
class WMDatabaseService(IWMDatabaseService):
    engine = None
    base = automap_base()
    observations = None

    def __init__(self, url, port, username, password, dbname):

        try:

            self.engine = create_engine(f"mariadb+mariadbconnector://{username}:{password}@{url}:{port}/{dbname}",
                                        echo=True)

            self.base.prepare(self.engine, reflect=True)
            self.observations = self.base.classes.observations

        except sqlalchemy.exc.TimeoutError:

            logging.error(f"Timeout connecting to database {url}:{port}/{dbname}")
            sys.exit()

        except sqlalchemy.exc.DBAPIError as ex:

            logging.error(f"Database access error: {ex}")
            sys.exit()

    def dispose(self):
        self.engine.dispose()

    # Gets the date of the  most recent observation from the observations table.
    # If there are no observations then the default observation date is returned.
    def get_most_recent_observation_date(self, default_observation_date: date):

        try:

            session = sqlalchemy.orm.sessionmaker()
            session.configure(bind=self.engine)
            session = session()
            result: datetime = session.query(func.max(self.observations.ObservationTime)).scalar()
            session.close()

            if result is None:
                return default_observation_date
            else:
                return result.date()

        except sqlalchemy.exc.DBAPIError as ex:

            logging.error(f"Database access error while getting most recent observation date: {ex}")
            sys.exit()

    # Saves observations to the database. Observations are provided as a list of hourly
    # observations for a multiple of days. These need to be reformatted before writing.
    def save_list_of_observations(self, observations):

        try:

            session = sqlalchemy.orm.sessionmaker()
            session.configure(bind=self.engine)
            session = session()

            for daily_observation in observations:

                _hourly_observation_counter = 0
                _date_of_observations = daily_observation["observations"][0]["obsTimeLocal"][0:10]

                for hourly_observation in daily_observation["observations"]:
                    session.add(self._create_formatted_observation(hourly_observation))
                    _hourly_observation_counter += 1

                if _hourly_observation_counter == 24:
                    logging.info(f"Observations recorded for {_date_of_observations}")
                else:
                    logging.warning(f"Only {_hourly_observation_counter} "
                                    f"observations were recorded for {_date_of_observations}")

            session.commit()
            session.close()

        except sqlalchemy.exc.DBAPIError as ex:

            logging.error(f"Database access error while saving list of observations: {ex}")
            sys.exit()

    # Creates and returns a single SQLAlchemy observation object from an hourly observation
    # that was returned from Weather Underground.
    def _create_formatted_observation(self, hourly_observation):

        return self.observations(ObservationTime=hourly_observation["obsTimeLocal"],
                                 SolarRadiationHigh=hourly_observation["solarRadiationHigh"],
                                 UvHigh=hourly_observation["uvHigh"],
                                 WindDirectionMean=hourly_observation["winddirAvg"],
                                 HumidityHigh=hourly_observation["humidityHigh"],
                                 HumidityLow=hourly_observation["humidityLow"],
                                 HumidityMean=hourly_observation["humidityAvg"],
                                 TemperatureHigh=hourly_observation["metric"]["tempHigh"],
                                 TemperatureLow=hourly_observation["metric"]["tempLow"],
                                 TemperatureMean=hourly_observation["metric"]["tempAvg"],
                                 WindSpeedHigh=hourly_observation["metric"]["windspeedHigh"],
                                 WindSpeedLow=hourly_observation["metric"]["windspeedLow"],
                                 WindSpeedMean=hourly_observation["metric"]["windspeedAvg"],
                                 WindGustHigh=hourly_observation["metric"]["windgustHigh"],
                                 WindGustLow=hourly_observation["metric"]["windgustLow"],
                                 WindGustMean=hourly_observation["metric"]["windgustAvg"],
                                 DewPointHigh=hourly_observation["metric"]["dewptHigh"],
                                 DewPointLow=hourly_observation["metric"]["dewptLow"],
                                 DewPointMean=hourly_observation["metric"]["dewptAvg"],
                                 WindChillHigh=hourly_observation["metric"]["windchillHigh"],
                                 WindChillLow=hourly_observation["metric"]["windchillLow"],
                                 WindChillMean=hourly_observation["metric"]["windchillAvg"],
                                 HeatIndexHigh=hourly_observation["metric"]["heatindexHigh"],
                                 HeatIndexLow=hourly_observation["metric"]["heatindexLow"],
                                 HeatIndexMean=hourly_observation["metric"]["heatindexAvg"],
                                 PressureHigh=hourly_observation["metric"]["pressureMax"],
                                 PressureLow=hourly_observation["metric"]["pressureMin"],
                                 PressureTrend=hourly_observation["metric"]["pressureTrend"],
                                 PrecipitationRate=hourly_observation["metric"]["precipRate"],
                                 PrecipitationTotal=hourly_observation["metric"]["precipTotal"]
                                 )
