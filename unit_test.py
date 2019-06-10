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


inputs1 = {
       'price': [221900, 538000, 180000, 604000, 510000],
       'city': ['phx', 'phx', 'phx', 'phx', 'phx'],
       'bedrooms': [2,2,3,3,2],
       'bathrooms': [2, 2, 3, 2, 1],
       'floors': [1, 2, 1, 2, 3],
       'waterfront': [0, 0, 0, 0, 1],
       'condition': [2, 3, 4, 1, 4],
       'sqft_basement': [1, 0,1, 0, 1],
       'yr_built': [1990, 1934, 1955, 1920, 2005],
       'yr_renovated': [0,0,0,1,1],
       'lot_log': [5650, 7242, 6000, 9780, 9500],
   }

inputs2 = {
       'price': [257500, 310000, 485000, 385000, 233000],
       'city': ['hou', 'hou', 'hou', 'hou', 'hou'],
       'bedrooms': [2,1,3,2,3],
       'bathrooms': [1, 2, 2, 3, 2],
       'floors': [3, 1, 2, 3, 1],
       'waterfront': [0, 1, 0, 0, 1],
       'condition': [3,4, 5, 2, 3],
       'sqft_basement': [1,0,0,1,0],
       'yr_built': [2007, 2012, 2001, 1999, 2000],
       'yr_renovated': [0,1,0,1,1],
       'lot_log': [5000, 6500, 3300, 2300, 5400],
   }
   
df1= pd.DataFrame(data=inputs1)
df2= pd.DataFrame(data=inputs2)
final = df1.append(df2)

yDict = [df1['price'], df2['price']]   #dictionary of y

xDict = [df1[['bedrooms', 'bathrooms',"floors", "waterfront", "condition", "sqft_basement", "yr_built", "yr_renovated", "lot_log"]],df2[['bedrooms', 'bathrooms',"floors", "waterfront", "condition", "sqft_basement", "yr_built", "yr_renovated", "lot_log"]]]   #dictionary of X


#tests for make_data

def test_append_cityNames():
    """Tests the append_cityNames function in make_data to ensure cities are properly appended."""
    zip_data = pd.DataFrame(columns=['price', 'zipcode'])
    prices = [1,2,3]
    zipcodes1 = [85258, 60201, 93953]
    zip_data['price'] = prices
    zip_data['zipcode'] = zipcodes1
    city_result = append_cityNames(zip_data, 'zipcode', 'city')
    assert type(city_result) is pd.core.frame.DataFrame
    assert city_result.shape == (3,3)


def test_choose_features():
    """Tests the choose_features function in make_data to ensure subsetting of dataframe is correct."""
    #city_result = append_cityNames(data, 'zipcode', 'city')
    columns = ["bedrooms", "bathrooms", "city"]
    feature_result = choose_features(final, columns)
    assert type(feature_result) is pd.core.frame.DataFrame
    assert feature_result.shape == (10, 3)

def test_log_variable():
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
    #feature_result = choose_features(data, columns)
    cities = ['phx', 'hou']
    x = final[['bedrooms', 'bathrooms', 'city']]
    split_result = splitDF_cities(x, cities)
    assert type(split_result) is list
    assert len(split_result) == len(cities)

def test_get_target():
    """Tests the get_target function to make sure the correct target is being returned."""
    #feature_result = choose_features(data, columns)
    #split_result = splitDF_cities(feature_result, cities)
    cities = ['phx', 'hou']
    split_result = [df1, df2]
    target_result = get_target(split_result, 'price')
    assert type(target_result) is list
    assert len(target_result) == len(cities)

def test_split_data():
    cities = ['phx', 'hou']
    split_result = split_data(xDict, yDict)
    assert type(split_result) is tuple
    assert len(split_result) == len(cities)  #has city lengh lists
    assert len(split_result[0]) == 2  #has test and train

def test_model_train():
    cities = ['phx', 'hou']
    d = {'model_train': {
       'choose_features': {
           #'num_years': final,
           'columns':  ["city", "bedrooms", "bathrooms","floors", "waterfront", "condition", "sqft_basement", "yr_built", "yr_renovated", "lot_log"]},
        'split_data':{
            'train_size': 0.7,
            'test_size': 0.3
        }
    }}
    models, finalxDict, finalyDict = model_train(xDict, yDict,**d['model_train'])
    with open('unitTest_model.pkl', "wb") as f:
        pickle.dump(models, f)
    assert len(models) == len(cities)
    assert type(models[0]) is sklearn.linear_model.base.LinearRegression

def test_model_score():
    with open('unitTest_model.pkl', 'rb') as f:
        models = pickle.load(f) 
    cities = ['phx', 'hou']
    x, y = split_data(xDict, yDict)
    scoring = model_score (models, x, y, cities)
    assert type(scoring) is pd.core.frame.DataFrame
    assert scoring.shape == (len(cities), 2)

def test_format_coefs():           
    cities = ['phx', 'hou']
    columns = ["bedrooms", "bathrooms", "floors", "waterfront", "condition", "sqft_basement", "yr_built", "yr_renovated", "lot_log"]
    with open('unitTest_model.pkl', 'rb') as f:
        models = pickle.load(f) 
    coefs = format_coefs(models, columns, cities)
    assert type(coefs) is pd.core.frame.DataFrame
    assert coefs.shape == (len(cities), len(columns))

## tests for application scripts

def test_input_prediction():
    """ Tests the prediction function from app.predict.py to ensure user inputs are predicted correctly"""
    with open('unitTest_model.pkl', 'rb') as f:
        models = pickle.load(f) 
    predict_result= prediction(models, 0, 4, 5, 3, 0, 4, 0, 1950, 0, 10000)
    assert type(predict_result) is str

def test_dec_price():
    """ Tests the decrease price function from app.decrease_price.py to ensure the correct output is being made"""
    with open('unitTest_model.pkl', 'rb') as f:
        models = pickle.load(f) 
    test_items, test_prices = dec_price(models, 0, 4, 5, 3, 0, 4, 0, 1950, 0, 10000)
    assert type(test_items) is list
    assert type(test_prices) is list
    assert len(test_items) == 2
    assert len(test_prices) == 8









