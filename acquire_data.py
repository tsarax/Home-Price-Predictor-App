
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import pandas as pd
import os
from os import path
import config
import boto3

def transferData():
   key_id = config.AWS_KEY_ID
   access_key = config.AWS_ACCESS_KEY
   copy_bucket = config.AWS_BUCKET
   copy_location = config.AWS_FILE_PATH

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
