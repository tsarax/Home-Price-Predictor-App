from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import pandas as pd
import os
from os import path
import argparse
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()

# class House(Base):
#     """create a table name Song with the following schema"""
#     __tablename__ = 'house'

#     index = Column(sql.Integer(), primary_key=True, autoincrement=True)
#     city = Column(String(80), nullable=False)
#     bedrooms = Column(sql.Float(), nullable=False)
#     bathrooms = Column(sql.Float(), nullable=False)
#     floors = Column(sql.Float(), nullable=False)
#     waterfront = Column(sql.Float())
#     condition = Column(sql.Float(), nullable=False)
#     sqft_basement = Column(sql.Float(), nullable=False)
#     yr_built = Column(sql.Float(), nullable=False)
#     yr_renovated = Column(sql.Float(), nullable=False)
#     lot_log = Column(sql.Float(), nullable=False)



#     def __repr__(self):
#         house_repr = "<(city='%s',bedrooms='%s', bathrooms='%s', floors='%s',  waterfront='%s', condition='%s',sqft_basement='%s', yr_built='%s', yr_renovated = '%s', sqft_lot='%s')>"
#         return house_repr % (self.city, self.bedrooms, self.bathrooms, self.floors,  self.waterfront, self.conditon, self.sqft_basement, self.yr_built, self.yr_renovated,self.sqft_lot)


class User(Base):
    """Where user inputs will be stored"""
    __tablename__ = 'user'

    index = Column(sql.Integer(), primary_key=True, autoincrement=True)
    city = Column(String(80), nullable=False)
    bedrooms = Column(sql.Float(), nullable=False)
    bathrooms = Column(sql.Float(), nullable=False)
    floors = Column(sql.Float(), nullable=False)
    waterfront = Column(sql.Float())
    condition = Column(sql.Float(), nullable=False)
    sqft_basement = Column(sql.Float(), nullable=False)
    yr_built = Column(sql.Float(), nullable=False)
    yr_renovated = Column(sql.Float(), nullable=False)
    lot_log = Column(sql.Float(), nullable=False)

    def __repr__(self):
        user_repr = "<(city='%s',bedrooms='%s', bathrooms='%s', floors='%s',  waterfront='%s', condition='%s',sqft_basement='%s', yr_built='%s', yr_renovated = '%s', sqft_lot='%s')>"
        return user_repr % (self.city, self.bedrooms, self.bathrooms, self.floors,  self.waterfront, self.conditon, self.sqft_basement, self.yr_built, self.yr_renovated,self.sqft_lot)


def create_db(args):
    # if args.user:
    if args.rds:
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        host = os.environ.get("MYSQL_HOST")
        port = os.environ.get("MYSQL_PORT")
        engine_string = "{}://{}:{}@{}:{}/msia423".\
        format(conn_type, user, password, host, port)
        engine = sql.create_engine(engine_string)
        Base.metadata.create_all(engine)
    else:
        engine_string_sqlite = 'sqlite:///user.db'
        engine_sqlite = sql.create_engine(engine_string_sqlite)
        Base.metadata.create_all(engine_sqlite)
    # else:       
    #     if args.rds:
    #         conn_type = "mysql+pymysql"
    #         user = os.environ.get("MYSQL_USER")
    #         password = os.environ.get("MYSQL_PASSWORD")
    #         host = os.environ.get("MYSQL_HOST")
    #         port = os.environ.get("MYSQL_PORT")
    #         engine_string = "{}://{}:{}@{}:{}/msia423".\
    #         format(conn_type, user, password, host, port)
    #         engine = sql.create_engine(engine_string)
    #         Base.metadata.create_all(engine)
    #     else:
    #         engine_string_sqlite = 'sqlite:///house.db'
    #         engine_sqlite = sql.create_engine(engine_string_sqlite)
    #         Base.metadata.create_all(engine_sqlite)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    parser.add_argument('--rds', default=False, help='path to yaml file with configurations')

    args = parser.parse_args()
    create_db(args)
                                                             