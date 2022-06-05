from IWMDatabaseService import IWMDatabaseService
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base


class WMDatabaseService(IWMDatabaseService):

    engine = None
    base = automap_base()
    observations = None

    def __init__(self, url, port, username, password):
        self.engine = create_engine(f"mysql://{username}:{password}@{url}:{port}", echo=True)

        self.base.prepare(self.engine, reflect=True)
        self.observations = self.base.classes.observations

    def get_most_recent_observation_date(self):
        result = self.engine.session.query(self.observations.ObservationTime,
                                           func.max(self.observations.ObservationTime))

        if result is None:
            return None
        else:
            return result.observations.observationtime

    def get_latest_observations(self):

        return "Not implemented"
