import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import zipcodes
from make_data import *
from train_model import *
from predict import *
from decrease_price import *
import pickle


data = pd.read_csv('data/raw_data.csv')
cities = ['SEATTLE', 'RENTON', 'BELLEVUE', 'KENT', 'REDMOND', 'KIRKLAND', 'AUBURN', 'SAMMAMISH', 'FEDERAL WAY', 'ISSAQUAH']
columns = ["city", "price", "bedrooms", "bathrooms", "sqft_lot", "floors", "condition", "waterfront", "sqft_basement", "yr_built", "yr_renovated"]

##do i have to change below??
with open("data/model.pkl", "rb") as f:
    models = pickle.load(f)

#tests for make_data

def test_append_cityNames():
    """Tests the append_cityNames function in make_data to ensure cities are properly appended."""
    city_result = append_cityNames(data, 'zipcode', 'city')
    assert type(city_result) is pd.core.frame.DataFrame
    assert city_result.shape == (21613, 22)


def test_choose_features():
    """Tests the choose_features function in make_data to ensure subsetting of dataframe is correct."""
    city_result = append_cityNames(data, 'zipcode', 'city')
    feature_result = choose_features(data, columns)
    assert type(feature_result) is pd.core.frame.DataFrame
    assert feature_result.shape == (21613, 11)

def test_log_variable() :
    """Tests the log_variable function in make_data to ensure variables are correctly being logged."""   
    df = pd.DataFrame(columns=['col1'])
    list1 = [1,2,3]
    df['col1'] = list1
    list2 = [np.log(1), np.log(2), np.log(3)]
    log_result = log_variable(df, 'logged', 'col1')
    print(log_result)
    assert log_result['logged'].tolist() == list2


def test_binary_var():
    """Tests the binary_var function in make_data to ensure variables are correctly being turned into binary variables"""
    df = pd.DataFrame(columns=['price', 'pools'])
    list1 = [1, 6, 4, 2.4, 0]
    list2 = [0, 4.5, 0, 1, 6]
    df['price']= list1
    df['pools']=list2
    results_binary = create_binary_var(df, 'pools')
    assert sum(((df['pools']==1) | (df['pools']==0))) == len(results_binary['pools'])


#tests for train_model

def test_splitDF_cities():
    """Tests the splitDF_cities function to make sure the dataframe is being split by city name."""
    feature_result = choose_features(data, columns)
    split_result = splitDF_cities(feature_result, cities)
    assert type(split_result) is list
    assert len(split_result) == len(cities)

def test_get_target():
    """Tests the get_target function to make sure the correct target is being returned."""
    feature_result = choose_features(data, columns)
    split_result = splitDF_cities(feature_result, cities)
    target_result = get_target(split_result, 'price')
    assert type(target_result) is list
    assert len(target_result) == len(cities)

def test_split_data():

def test_model_train():

def test_model_score():


def test_format_coefs():           


## tests for application scripts

def test_input_prediction():
    """ Tests the prediction function from app.predict.py to ensure user inputs are predicted correctly"""
    predict_result= prediction(models, 0, 4, 5, 3, 0, 4, 0, 1950, 0, 10000)
    assert predict_result == "$1,593,093"

def test_dec_price():
    """ Tests the decrease price function from app.decrease_price.py to ensure the correct output is being made"""
    test_items, test_prices = dec_price(models, 0, 4, 5, 3, 0, 4, 0, 1950, 0, 10000)
    assert type(test_items) is list
    assert type(test_prices) is list
    assert len(test_items) == 2
    assert len(test_prices) == 8









