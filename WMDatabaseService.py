import sqlalchemy
from sqlalchemy import create_engine

class WMDatabaseService:
    def __init__(self, url, port, username, password):
        engine = create_engine(f"mysql://{username}:{password}@{url}",echo=True)

    def check_that_wu_is_recording(self):
        connection = self.engine.connect()

        if connection.

    def get_most_recent_observation_date:
        pass

    def get_latest_observations:
        pass
