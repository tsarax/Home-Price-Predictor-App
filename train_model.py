import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sklearn
import zipcodes
import sys
import os
import json
import warnings
import yaml
import argparse
import pickle
import logging 
from make_data import choose_features

logger = logging.getLogger(__name__)


def splitDF_cities(df, city_list):
    """Splits dataframe into a dictionary of dataframes by city. 
    
    Arguments:
        df {DataFrame} -- Dataframe containing a city column 
        city_list {Str, list} -- List of cities that are in the dataframe to split dataframe into sub-dataframes. 
    
    Returns:
        cityDict {Dictionary} -- Dictionary of city specific dataframes
    """
    #first city in the city list will have index of 0 in the cityDict, and so on. 
    cityDict=[]
    logger.info("the dataframe is appending city names for %s cities", len(city_list))
    for i in city_list: #loop through cities
        df1 = df[df.city== i]  #get data for that city
        cityDict.append(df1)
    return cityDict    

def get_target(df_dict, target, save_path=None):
    """Takes in a dictionary of dataframes and finds the target variable in each dataframe. 
    
    Arguments:
        df_dict {Dictonary} -- Dictionary of city specific dataframes
        target {str} -- Name of the target column
    
    Keyword Arguments:
        save_path {str} -- Optional path to save the dictionary of targets to. (default: {None})
    
    Returns:
        yDict {Dictionary} -- Dictionary of dataframe target variables, indexed by the city list. 
    """
    yDict = [] 
    for i in range(len(df_dict)):  #loop through the dictionary of city dfs to get each target
        df1 = df_dict[i][target]
        yDict.append(df1)
    
    if save_path is not None:  #optional saving 
        yDict.to_csv(save_path, header=True)
        logger.info("the target data was saved to %s", save_path)


    return yDict

def split_data(XDict, yDict, path_xDict=None, path_yDict=None, train_size=0.7, test_size=0.3, random_state=24):
    """Splits dictionary of dataframes into train and test sizes within each dataframe. 
    
    Arguments:
        XDict {Dictionary} -- Dictionary of dataframes with feature variables, indexed by the city list. 
        yDict {Dictionary} -- Dictionary of dataframe target variables, indexed by the city list. 
    
    Keyword Arguments:
        path_xDict {str} -- Optional path to save dictionary of split city dataframes for feature variables. (default:{None})
        path_yDict {str} -- Optional path to save dictionary of split city dataframes for target variable. (default:{None})
        train_size {float} -- Fraction of data to use for testing (default: {0.7})
        test_size {float} -- Fraction of data to use for training (default: {0.3})
        random_state {int} -- Random state to obtain same results each time. (default: {24})

    Returns:
        finalxDict {Dictionary} -- Dictionary of dictionaries. Each dictionary is for a city and contains the test and train feature data for that city.
        finalyDict {Dictionary} -- Dictionary of dictionaries. Each dictionary is for a city and contains the test and train target data for that city.
    """
    finalxDict = []
    finalyDict = []
    for i in range(len(XDict)): #loops through the dictionary of dataframes to get each individual dataframe 
        cityX= XDict[i]   #dataframe of features for the city i 
        cityy= yDict[i]   #target dataframe for city i
        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(cityX, cityy, train_size=0.7, random_state=random_state)  #splits according to test size

        #make dict for each city that contains train and test dataframes
        X= dict(train=X_train)  
        y= dict(train=y_train)
        #adds test to dictionary
        if len(X_test) > 0:
            X["test"] = X_test
            y["test"] = y_test
        finalxDict.append(X)
        finalyDict.append(y)
    #save x and y dict
    if path_xDict is not None:
        finalxDict.to_csv(path_xDict)
        logger.info("final x dictionary saved to %s", path_xDict)
    if path_yDict is not None:    
        finalyDict.to_csv(path_yDict)
        logger.info("final y dictionary saved to %s", path_yDict)

    return finalxDict, finalyDict

def model_train(xDict, yDict, **kwargs):
    """Train each city model and save a dictionary of models to a pickle.
    
    Arguments:
        xDict {Dictionary} -- Dictionary of dataframes with feature variables split into test and train, indexed by the city list. 
        yDict {Dictionary} --  Dictionary of dataframes with target variable split into test and train, indexed by the city list. 
    
    
    Returns:
        models {Model} -- All models of the cities
        finalxDict {Dictionary} -- Dictionary of dataframes with feature variables split into test and train, indexed by the city list. 
        finalyDict {Dictionary} -- Dictionary of dataframes with target variable split into test and train, indexed by the city list. 
    """
    x_final = []
    #choose features for training according to config yml file. 
    for i in range(len(xDict)):
        X = xDict[i]
        X = choose_features(X, **kwargs["choose_features"])
        x_final.append(X)
    logger.info("length of x features is  %s", len(x_final))    

    #split data    
    finalxDict, finalyDict = split_data(x_final, yDict, **kwargs["split_data"])
    #create list of models for each city
    models = []
    for i in range(len(finalxDict)):
        X = finalxDict[i]
        y = finalyDict[i]
        model = LinearRegression()
        X_train = X["train"].iloc[:, 0:10]
        y_train = y["train"]

        model.fit(X_train, y_train)  
        models.append(model)
    logger.info("%s models made for cities", len(models))    

    

    return models, finalxDict, finalyDict


def model_score(models, xDict, yDict, city_list, path_results=None, **kwargs):
    """Scores the model to find r-squared of train and test
    
    Arguments:
        models {List} -- List of models
        xDict {Dictionary} -- Dictionary of dataframes with feature variables split into test and train, indexed by the city list. 
        yDict {Dictionary} -- Dictionary of dataframes with target variable split into test and train, indexed by the city list. 
        city_list {str, list} -- List of cities in same order that dataframe was indexed by. 
    
    Keyword Arguments:
        path_results {str} -- Where to save results csv to (default: {None})
    
    Returns:
        results{dataframe} -- Dataframe containing r-squared for test and train of each city model. 
    """

    r2Train_list = []
    r2Test_list = []
    #gets r-squred for both test and train sets.
    for i in range(len(xDict)):
        model = models[i]
        x_test = xDict[i]["test"]
        y_test = yDict[i]["test"]
        x_train = xDict[i]["train"]
        y_train = yDict[i]["train"]
        r2Train = model.score(x_train, y_train)
        r2Test = model.score(x_test, y_test)
        r2Train_list.append(r2Train)
        r2Test_list.append(r2Test)
    
    #appends results to dataframe
    results = pd.DataFrame(index = city_list)
    results['r2_Train'] = r2Train_list
    results['r2_Test'] = r2Test_list

    if path_results is not None:
        results.to_csv(path_results)
        logger.info("Model scoring results are saved to %s", path_results)

    return results


def format_coefs(models, columns, city_list, path_save=None):
    """ Find coeficients and create a dataframe with them.
    
    Arguments:
        models {List} -- List of models for each city.
        columns {str, list} -- List of what to name columns for each coefficient, should be feature variables trained on.
        path_save {str} -- path to save coefficients to. (default: {None})
        city_list {str, List} -- List of cities used in model. 
    
    Returns:
        coefdf{dataframe} -- Dataframe with all coeficients for variables and cities. 
    """
    coefs = []
    #loop through models and grab coefficients for each.
    for i in range(len(models)): 
        model1 = models[i]
        coef1 = model1.coef_
        coefs.append(coef1)
    #format coeficients into dataframe with relative variable names and cities     
    coefdf = pd.DataFrame(coefs)
    coefdf.columns= columns
    coefdf.index = city_list
    if path_save is not None:
        coefdf.to_csv(path_save)
        logger.info("coeficient data saved to %s", path_save)

    return coefdf




def run_train(args):
    """Orchestrates the training of the model using command line arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f)
    path = args.output
    config_try = config['train_model']   
    if args.input is not None:
        df = pd.read_csv(args.input)
        logger.info("Features for input into model loaded from %s", args.input)
    else:
        raise ValueError("Path to CSV for input data must be provided through --input for training.")
    

    df_dict = splitDF_cities(df, **config_try['splitDF_cities'])
    yDict = get_target(df_dict, **config_try['get_target'])

    models, xDict, yDict = model_train(df_dict, yDict, path, **config_try['model_train'])

    #save model to output argument path
    if args.output is not None:
        with open(args.output, "wb") as f:
            pickle.dump(models, f)
            logger.info("Trained model object saved to %s", args.output)    
    else:
        raise ValueError("Path to save models must be given with --output to use for app running.")        


    columns = xDict[0]['train'].columns
    results = model_score(models, xDict, yDict, **config_try['model_score'])
    coefdf = format_coefs(models, columns, **config_try['format_coefs'])      

  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train models for each city to predict price")
    parser.add_argument('--config', help='path to yaml file with configurations', default="config.yml")
    parser.add_argument('--input', help='path to features data', default='data/data_features.csv')
    parser.add_argument("--output",  default="data/model.pkl",
                        help="Path to saving models.")
    args = parser.parse_args()


    run_train(args)      