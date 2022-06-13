# Loads data from a given json file into a given database table.
# Used to unit test the WMDatabaseService.

import configparser
import sqlalchemy.orm

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base


def load_test_database(data_file):
    # Configure the database

    config = configparser.ConfigParser()
    config.read(Path().resolve().parent + '/' + 'config.ini')

    engine = create_engine(f"mariadb+mariadbconnector://"
                           f"{config.get('Database', 'UserId')}:{config.get('Database', 'Password')}"
                           f"@{config.get('Database', 'IPAddress')}:{config.get('Database', 'Port')}"
                           f"/{config.get('Database', 'DatabaseName')}",
                           echo=True)

    base = automap_base()
    base.prepare(engine, reflect=True)

    observations = base.classes.observations

    session = sqlalchemy.orm.sessionmaker()
    session.configure(bind=engine)
    session = session()

    # Delete existing contents of table
    observations.query.delete()

    # Add new rows

    # Finalise

    session.commit()
