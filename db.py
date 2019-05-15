from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import pandas as pd
import os
from os import path
import config

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class House(Base):
    """create a table name Song with the following schema"""
    __tablename__ = 'house'

    index = Column(sql.Integer(), primary_key=True, autoincrement=True)
    bedrooms = Column(sql.Float(), nullable=False)
    bathrooms = Column(sql.Float(), nullable=False)
    sqft_lot = Column(sql.Float(), nullable=False)
    floors = Column(sql.Float(), nullable=False)
    condition = Column(sql.Float(), nullable=False)
    waterfront = Column(sql.Float())
    sqft_basement = Column(sql.Float(), nullable=False)
    yr_built = Column(sql.Float(), nullable=False)
    yr_renovated = Column(sql.Float(), nullable=False)
    city = Column(String(80), nullable=False)


    def __repr__(self):
        house_repr = "<(bedrooms='%s', bathrooms='%s', sqft_lot='%s', floors='%s', condition='%s', waterfront='%s', sqft_basement='%s', yr_built='%s', yr_renovated = '%s')>"
        return house_repr % ( self.bedrooms, self.bathrooms, self.sqft_lot, self.floors, self.conditon, self.waterfront, self.sqft_basement, self.yr_built, self.yr_renovated)


def create_db(rds=False):  
    if rds:
        conn_type = "mysql+pymysql"
        user = config.MYSQL_USER
        password = config.MYSQL_PASSWORD
        host = config.MYSQL_HOST
        port = config.MYSQL_PORT
        engine_string = "{}://{}:{}@{}:{}/msia423".\
        format(conn_type, user, password, host, port)
        engine = sql.create_engine(engine_string)
        Base.metadata.create_all(engine)
    else:     
        engine_string_sqlite = 'sqlite:///house.db'
        engine_sqlite = sql.create_engine(engine_string_sqlite)
        Base.metadata.create_all(engine_sqlite)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    parser.add_argument('--rds', default=False, help='path to yaml file with configurations')
    args = parser.parse_args()
    create_db(args.rds)
