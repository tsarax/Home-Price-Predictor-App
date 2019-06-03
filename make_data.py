import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import zipcodes
import sys
import os
import json
import warnings
import yaml
import argparse
import logging 
import seaborn as sns
import boto3

logger = logging.getLogger(__name__)


def get_s3(bucket, file_path, download_path, **kwargs):
    """Downloads data from an S3 bucket.
    
    Arguments:
        bucket {String} -- S3 Bucket name where data is stored
        file_path {String} -- Path to data within S3 Bucket
        download_path {String} -- Path to save data to
    """
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(bucket)
    bucket.download_file(file_path, download_path)
    logger.info("The data has been downloaded from S3 and is stored in %s", file_path)


def load_data(path):
    """Loads in data from specified path. 
    
    Arguments:
        path {String} -- path to find the file
    
    Returns:
        data {DataFrame} -- Dataframe of data read in
    """
    data = pd.read_csv(path)
    return data


def create_binary_var(df, variable, threshold=0):
    """Creates a binary variable for an existing variable. Ones are given to values that are not equal to the
    threshold. 
    
    Arguments:
        df {dataframe} -- dataframe that contains variable for change. 
        variable {string} -- Which variable needs to be turned into binary
        threshold {int} -- Number to decide if variable should be 0 or 1. 
    Returns:
        df {DataFrame} -- Dataframe with changed variable.     
    """
    if type(variable) == str:  #if input is only for one variable
        df.loc[df[variable] != threshold, variable] = 1
    else:     
        for i in range(len(variable)):   #if input is a list -- to be done for multiple variable creation
            df.loc[df[variable[i]] != threshold, variable[i]] = 1
    return df

def append_cityNames(df, zipColumn, cityColName):
    """Adds names of cities to a dataframe that contains zip codes. 
    
    Arguments:
        df {dataframe} -- dataframe containing zip codes and cities to be appended to. 
        zipColumn {string} -- Existing column name of zip codes
        cityColName {string} -- Name of column to place cities in
    
    Returns:
        df {DataFrame} -- Dataframe with appended city names. 
    """
    cities = []
    for i in df[zipColumn]:  #loops through zipcodes and finds matching city name 
        code = i
        code = str(code)
        city = zipcodes.matching(code)[0]['city']
        cities.append(city)
    df[cityColName] = cities  #append to dataframe
    logger.info("Cities were appended to the dataframe.")
    return df 

def log_variable(df, new_col_name, column): 
    """Generate new feature for logged column.
    
    Arguments:
        df {dataframe} -- Dataframe to append column(s) to and contains the column to log. 
        new_col_name {string} -- Name for the newly generated column(s). 
        column {string} -- Column name(s) for logging. 
    
    Returns:
        df {dataframe} -- Output dataframe containing new column(s).
    """
    if type(new_col_name) == str:    #if input is only for one variable
        df[new_col_name] = np.log(df[column])
        logger.info("The following column was logged: %s", column)


    else: 
        for i in range(len(new_col_name)):  #if input is a list -- to be done for multiple variable creation
            name = new_col_name[i]
            col1 = column[i]
            df[name] = np.log(df[col1])
        logger.info("The following columns were logged: %s", ",".join(column))
    
    return df


def choose_features(df, features_to_use=None, target=None, save_path=None, **kwargs):
    """Reduces the dataset to the features_to_use. Will keep the target if provided.
    Args:
        df (:py:class:`pandas.DataFrame`): DataFrame containing the features
        features_to_use (:obj:`list`): List of columnms to extract from the dataset to be features
        target (str, optional): If given, will include the target column in the output dataset as well.
        save_path (str, optional): If given, will save the feature set (and target, if applicable) to the given path.
        **kwargs:
    Returns:
        X (:py:class:`pandas.DataFrame`): DataFrame containing extracted features (and target, it applicable)
    """

    logger.debug("Choosing features")
    if features_to_use is not None:
        features = []
        dropped_columns = []
        for column in df.columns:
            # Identifies if this column is in the features to use or if it is a dummy of one of the features to use
            if column in features_to_use or column.split("_dummy_")[0] in features_to_use or column == target:
                features.append(column)
            else:
                dropped_columns.append(column)

        if len(dropped_columns) > 0:   
            logger.info("The following columns were not used as features: %s", ",".join(dropped_columns))
        logger.debug(features)
        X = df[features]
    else:
        logger.debug("features_to_use is None, df being returned")
        X = df

    if save_path is not None:
        X.to_csv(save_path, **kwargs)

    return X


def run_data(args):
    """ Orchestrates obtaining data and feature engineering"""
    with open(args.config, "r") as f:
        config = yaml.load(f)

    config_try = config['make_data']   #set up config

    #load data
    get_s3(**config_try['get_s3'])
    df = load_data(**config_try['load_data'])

    #create variables
    df = create_binary_var(df, **config_try['create_binary_var'])
    df = append_cityNames(df, **config_try['append_cityNames'])
    df = log_variable(df, **config_try['log_variable'])
    df = choose_features(df, **config_try['choose_features'])

    if args.output is not None:
       df.to_csv(args.output, index=False) 
       logger.info("Features for output saved to %s", args.output)
    else:
        raise ValueError("Path to CSV for output feature data must be provided through --output to move forward with training.")
   



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict cloud class")
    parser.add_argument('--config', help='path to yaml file with configurations', default="config.yml")
    parser.add_argument("--output",  default="data/data_features.csv",
                        help="Path to where to save data for training")
    args = parser.parse_args()


    run_data(args)        