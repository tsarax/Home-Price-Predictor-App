import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import zipcodes
from make_data import append_cityNames, choose_features
from train_model import splitDF_cities, get_target
from predict import prediction
from decrease_price import dec_price


data = pd.read_csv('data/raw_data.csv')
cities = ['SEATTLE', 'RENTON', 'BELLEVUE', 'KENT', 'REDMOND', 'KIRKLAND', 'AUBURN', 'SAMMAMISH', 'FEDERAL WAY', 'ISSAQUAH']
columns = ["city", "price", "bedrooms", "bathrooms", "sqft_lot", "floors", "condition", "waterfront", "sqft_basement", "yr_built", "yr_renovated"]



def test_append_cityNames():
    """Tests the append_cityNames function in make_data to ensure cities are properly appended."""
    city_result = append_cityNames(data, 'zipcode', 'city')
    assert type(city_result) is pd.core.frame.DataFrame
    assert city_result.shape == (21613, 22)


def test_choose_features():
    """Tests the choose_features function in train_model to ensure subsetting of dataframe is correct."""
    city_result = append_cityNames(data, 'zipcode', 'city')
    feature_result = choose_features(data, columns)
    assert type(feature_result) is pd.core.frame.DataFrame
    assert feature_result.shape == (21613, 11)


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

## testing application scripts

def test_input_prediction():
    """ Tests the prediction function from app.predict.py to ensure user inputs are predicted correctly"""
    predict_result= prediction(0, 4, 5, 3, 0, 4, 0, 1950, 0, 10000)
    assert predict_result == '$1,575,427'

def test_dec_price():
    """ Tests the decrease price function from app.decrease_price.py to ensure the correct output is being made"""
    test_items, test_prices = dec_price(0, 4, 5, 3, 0, 4, 0, 1950, 0, 10000)
    assert type(test_items) is list
    assert type(test_prices) is list
    assert len(test_items) == 2
    assert len(test_prices) == 8









