import sqlalchemy as db

from sqlalchemy import create_engine, update
from sqlalchemy.engine import URL
from sqlalchemy.sql import text

import Config
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
    __tablename__ = "drinks"

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(Integer)
    price = Column(Float)
    color = Column(String, nullable = True)
    description = Column(String, nullable = True, default = "No description.")

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
        # query = f"UPDATE {self.__tablename__} SET description='gaming' WHERE name='{self.drink.name}'"
        # session.execute(text(query))
        # session.commit()

    def update(self):
        drink = self.drink
        query = f"UPDATE {self.__tablename__} SET description='gaming' WHERE name='{drink.name}'"
        session.execute(text(query))
        session.commit()


Base.metadata.create_all(engine)

if __name__ == "__main__":

    db = DrinkDBEntry(Drink("Test drin2k", 1.23, "No color"))
    session.add(db)
    session.commit()
    db.update()
