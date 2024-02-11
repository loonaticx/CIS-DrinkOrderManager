"""
DatabaseManager is the kickstart engine for connecting and working with the database.

You shouldn't need to import it more than once since it serves as the driver code. (Be mindful where it's imported!)
"""

import sqlalchemy as db

from sqlalchemy import create_engine, update
from sqlalchemy.engine import URL
from sqlalchemy.sql import text

from config import Config
from base.ConnectionType import ConnectionType
from base.Drink import Drink
import sys

if Config.CONNECTION_MODE == ConnectionType.LOCAL_MEMORY:
    engine = create_engine("sqlite:///:memory:", echo = Config.VERBOSE_OUTPUT)
elif Config.CONNECTION_MODE == ConnectionType.LOCAL_FILE:
    engine = create_engine("sqlite:///drinks.db", echo = Config.VERBOSE_OUTPUT)
elif Config.CONNECTION_MODE == ConnectionType.REMOTE_SERVER:
    url_object = URL.create(
        "mysql+mysqldb",
        username = Config.REMOTE_USERNAME,
        password = Config.REMOTE_PASSWORD,
        host = Config.REMOTE_HOST,
        database = Config.SCHEMA,
    )
    # For "production", do not echo to output regardless if we have verbose mode on or not.
    engine = create_engine(url_object, echo = False)
else:
    print("ERROR: Config value CONNECTION_MODE is not recognized. Check your config file!")
    sys.exit()

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = engine)
session = Session()

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String, Float


class DrinkDBEntry(Base):
    """
    Skeleton for a db entry in the "drinks" table.

    Will be added into the database upon init
    """

    __tablename__ = "drinks"

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(64))
    price = Column(Float)
    color = Column(String(32), nullable = True)
    description = Column(String(128), nullable = True, default = "No description.")

    def __init__(self, drink: Drink):
        self.drink = drink
        self.name = drink.name
        self.price = drink.price
        self.color = drink.color
        self.description = drink.description
        self._generate_db_entry()

    def __repr__(self):
        return "<DrinkDBEntry(name='%s', price='%s', id='%s')>" % (
            self.name,
            self.price,
            self.id,
        )

    def _generate_db_entry(self):
        session.add(self)
        session.commit()


# Creates the "drinks" table if not done so already
Base.metadata.create_all(engine)

if __name__ == "__main__":
    # Test adding entries into the db
    db = DrinkDBEntry(Drink("Test drin2k", 1.23, "No color"))
