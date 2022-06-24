import sqlalchemy.orm

from IWMDatabaseService import IWMDatabaseService
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base


class WMDatabaseService(IWMDatabaseService):

    engine = None
    base = automap_base()
    observations = None

    def __init__(self, url, port, username, password, dbname):
        self.engine = create_engine(f"mariadb+mariadbconnector://{username}:{password}@{url}:{port}/{dbname}",
                                    echo=True)

        self.base.prepare(self.engine, reflect=True)
        self.observations = self.base.classes.observations

    def dispose(self):
        self.engine.dispose()

    # Gets the date of the  most recent observation from the observations table.
    # If there are no observations then the default observation date is returned.
    def get_most_recent_observation_date(self, default_observation_date):

        session = sqlalchemy.orm.sessionmaker()
        session.configure(bind=self.engine)
        session = session()
        result = session.query(func.max(self.observations.ObservationTime)).scalar()
        session.close()

        if result is None:
            return default_observation_date
        else:
            return result

    def get_latest_observations(self):

        return "Not implemented"
