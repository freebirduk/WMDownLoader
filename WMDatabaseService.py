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

    def get_most_recent_observation_date(self):

        session = sqlalchemy.orm.sessionmaker()
        session.configure(bind=self.engine)
        session = session()
        temp = session.query(self.observations).all()
        result = session.query(func.max(self.observations.ObservationTime)).scalar()
        session.close()

        if result is None:
            return None
        else:
            return result.observations.observationtime

    def get_latest_observations(self):

        return "Not implemented"
