import pandas as pd
import numpy as np
import os
from scipy import stats
from scipy.stats import norm
from sqlalchemy import create_engine
import logging
import pickle

logger = logging.getLogger(__name__)

def list_creation(input1):
    """Creates lists for each individual attribute change so we can test one change at a time.
    
    Arguments:
        input1 {list} -- List of the user input attribute values. 
    
    Returns:
        list1 {list} -- List of lists containing each attribute values and one change in each list. 
    """
    if len(input1) != 9:
        logger.warning("not all inputs were passed to create the sublists for attribuet changes.")
    #copy input list to make sublists
    trybeds = input1.copy()
    trybaths = input1.copy()
    tryfloors= input1.copy()
    trywater = input1.copy()
    trycondition= input1.copy()
    trybasement = input1.copy()
    tryreno = input1.copy()
    trysqft = input1.copy()

    #logic for changing inidividual attribute values. Nothing less than 0 or less than 1 if a count(beds, baths, floors, condition)
    #no changing for the year built.
    #lot square footage only changes if greater than 1000 (6 logged) 
    if input1[0] >1: 
        trybeds[0] = trybeds[0]  - 1
    elif input1[0] == 1:
        trybeds[0] = trybeds[0]
           
    if input1[1] >1: 
        trybaths[1] = trybaths[1] - 1
    elif input1[1] == 1:
        trybaths[1] = trybaths[1]    
        
    if input1[2] > 1:
        tryfloors[2]= tryfloors[2] -1
    elif input1[2] == 1:
        tryfloors[2] = tryfloors[2]
    
    if input1[3] == 1:
        trywater[3]= trywater[3] -1
    elif input1[3] != 1:
        trywater[3] = trywater[3]
    
    if input1[4] >1:     
        trycondition[4]= trycondition[4] -1
    elif input1[4] == 1:
        trycondition[4] = trycondition[4]
    
    if input1[5] == 1:
        trybasement[5]= trybasement[5] -1    
    elif input1[5] != 1:
        trybasement[5] = trybasement[5]
        
    if input1[7] == 1:
        tryreno[7]= tryreno[7]-1
    elif input1[7] != 1:
        tryreno[7] = tryreno[7]

    if input1[8] > np.log(1000):
        trysqft[8]= trysqft[8] - trysqft[8]*.05
    else: trysqft[8] = trysqft[8]   
    
    #create a list of each individual list
    list1=[trybeds,trybaths,tryfloors, trywater, trycondition, trybasement, tryreno, trysqft]
    return list1


def decreased_price_w(m, l):
    """Finds the attribute and value of the attribute responsible for the minimum price. 
    
    Arguments:
        m {int} -- index of the minimum price 
        l {list of list} -- output from list_creation, contains the list of inputs with each attribute changed once. 
    
    Returns:
        item_list {str, list} -- Indicates which attribute to change and to which value. 
    """
    min_index=m
    list1=l
    #get list that resulted in the minimum price, index by min_index(m) -- will tell what value attribute changed to
    picked_list = list1[min_index]
    item_list = []
    #find what the min_index is -- tells which attribute change worked 
    if min_index == 0:
        item_list.append('bedrooms')
        item_list.append(picked_list[0])
    if min_index == 1:
        item_list.append('bathrooms')
        item_list.append(picked_list[1])
    if min_index == 2:
        item_list.append('floors')
        item_list.append(picked_list[2])
    if min_index == 3:
        item_list.append('waterfront')
        item_list.append('none') 
    if min_index == 4:
        item_list.append('condition')
        item_list.append(picked_list[3])
    if min_index == 5:
        item_list.append('basement')
        item_list.append('none')  
    if min_index == 7:
        item_list.append('renovation')
        item_list.append('none')  
    if min_index == 8:
        item_list.append('lot square footage')
        item_list.append(np.exp(picked_list[8]))      
        
    if len(item_list) != 2:
        logger.warning("Item list returned does not contain both the attribute and the change, it is length: %s", len(item_list))    
    return item_list    


def dec_price(model, city, bedrooms, bathrooms, floors, waterfront, condition, sqft_basement, yr_built, yr_renovated, lot_log):
    """Takes user input and finds an attribute to change and the value to change it to in order to lower price most.
    
    Arguments:
        city {int} -- selected city for model index
        bedrooms {int}  -- bedroom count
        bathrooms{int} -- bathroom count
        floors {int}  -- floor count
        waterfront {int}  -- binary variable for waterfront
        condition {int}  -- condition of home
        sqft_basement {int}  -- binary variable for basement
        yr_built {int}  -- year built
        yr_renovated {int}  -- binary variable for renovations
        lot_log {int}  -- sqft of lot
    
    Returns:
        items {str, list} -- List containing attribute to change and what to change it to. 
        prices {int} -- price of house when attribute is changed. 
    """
    model = model[int(city)]
    lot_log = np.log(int(lot_log))  #Take log of user input -- how it is in model.

    #set user_input format
    user_input = [int(bedrooms), int(bathrooms), int(floors), int(waterfront), int(condition), int(sqft_basement), int(yr_built), int(yr_renovated), lot_log]
    
    #get list of lists for attribute changes
    list1 = list_creation(user_input)
    prices=[]
    #turn each sublist into dataframe and predict price, append to list
    for i in range(len(list1)):
        try_list = list1[i]
        selection=[{'bedrooms': try_list[0], 'bathrooms': try_list[1], 'floors' :try_list[2], 'waterfront': try_list[3], 'condition':try_list[4], 'sqft_basement':try_list[5], 'yr_built':try_list[6], 'yr_renovated':try_list[7], 'lot_log':try_list[8] }]
        df = pd.DataFrame(selection,  columns= ['bedrooms', 'bathrooms', 'floors', 'waterfront', 'condition', 'sqft_basement', 'yr_built', 'yr_renovated', 'lot_log'])
        preds = model.predict(df)
        prices.append(preds)
    if len(prices) != 8:
        logger.warning("Price list is not of length 8, it is of length: %s", len(prices))    

    
    min_index = prices.index(min(prices))   #find index of the minimum price
    items = decreased_price_w(min_index, list1)  #find attribute and value change that results in the minimum price
    
    return items, prices