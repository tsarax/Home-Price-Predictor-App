
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import pandas as pd
import os
from os import path
import config_db
import boto3
import argparse

def transferData():
   key_id = config_db.AWS_KEY_ID
   access_key = config_db.AWS_ACCESS_KEY
   copy_bucket = config_db.AWS_BUCKET
   copy_location = config_db.AWS_FILE_PATH

   s3 = boto3.resource('s3',
        aws_access_key_id=key_id,
        aws_secret_access_key= access_key)

   copy_source = {
       'Bucket': 'nw-tovasimonson-oregon',
       'Key': 'kc_house_data.csv'
   }
   s3.meta.client.copy(copy_source, copy_bucket, copy_location)

if __name__ == "__main__":
    transferData()   
