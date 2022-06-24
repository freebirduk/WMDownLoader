# Loads data from a given json file into a given database table.
# Used to unit test the WMDatabaseService.

import json
import pandas
import sqlalchemy.orm

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base


class MaintainTestDatabase:
    config = None

    def __init__(self, configuration_data):

        # Read in configuration data
        self.config = configuration_data

    def load_test_database(self, data_file):

        # Configure database and ORM
        engine = create_engine(f"mariadb+mariadbconnector://"
                               f"{self.config.get('Database', 'UserId')}"
                               f":{self.config.get('Database', 'Password')}"
                               f"@{self.config.get('Database', 'IPAddress')}"
                               f":{self.config.get('Database', 'Port')}"
                               f"/{self.config.get('Database', 'DatabaseName')}",
                               echo=True)

        base = automap_base()
        base.prepare(engine, reflect=True)

        observations = base.classes.observations

        session = sqlalchemy.orm.sessionmaker()
        session.configure(bind=engine)
        session = session()
        # Delete existing contents of table
        session.query(observations).delete()

        session.commit()

        # Add new rows (unless no JSON data file specified)
        if data_file is not None:
            try:
                json_file = open(data_file)
                json_data = json.loads(json_file.read())

                data_frame = pandas.DataFrame(json_data)
                data_frame = data_frame.loc[:, data_frame.columns != "ObservationId"]

                data_frame.to_sql("observations", engine, if_exists='append', index=False)

                json_file.close()

            except IOError:
                return False

        # Finalise

        engine.dispose()

        return True
