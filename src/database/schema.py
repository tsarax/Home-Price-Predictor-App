import config
import logging.config
import yaml

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker

from src.helpers.helpers import create_connection, get_session


logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


class House(Base):
    """create a table name Song with the following schema"""
    __tablename__ = 'house'

    index = Column(Integer, primary_key=True, autoincrement=True)
    bedrooms = Column(Float, nullable=False)
    bathrooms = Column(Float, nullable=False)
    sqft_lot = Column(Float, nullable=False)
    floors = Column(Float, nullable=False)
    condition = Column(Float, nullable=False)
    waterfront = Column(Float)
    sqft_basement = Column(Float, nullable=False)
    yr_built = Column(Float, nullable=False)
    yr_renovated = Column(Float, nullable=False)
    city = Column(String(80), nullable=False)


    def __repr__(self):
        house_repr = "<(bedrooms='%s', bathrooms='%s', sqft_lot='%s', floors='%s', condition='%s', waterfront='%s', sqft_basement='%s', yr_built='%s', yr_renovated = '%s')>"
        return house_repr % ( self.bedrooms, self.bathrooms, self.sqft_lot, self.floors, self.conditon, self.waterfront, self.sqft_basement, self.yr_built, self.yr_renovated)


def create_db():
    """Creates a database with rates from the api
    Returns: None
    """
    engine = create_connection(dbconfig=config.DBCONFIG)
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logger.info("Database created with tables")        

def persist_data(beds,baths, lot, floors, cond, water, basement, yr, reno, city)
    session = get_session(dbconfig=config.DBCONFIG)
    #ARIMA_Params.query.filter_by(CURRENCY=currency).delete()
    params = House(bedrooms=beds, bathrooms=baths, lot=sqft_lot, floors= floors, conditon=cond, waterfront=water, sqft_basement=basement, yr_built=yr, yr_renovated=reno, city=city)

    session.add(params)
    session.commit()
    logger.info("loaded in the db")
