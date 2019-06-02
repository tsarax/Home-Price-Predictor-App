import pandas as pd
import numpy as np
import os
from scipy import stats
from scipy.stats import norm
from sqlalchemy import create_engine
import logging
import pickle

logger = logging.getLogger(__name__)

def prediction(model, city, bedrooms, bathrooms, floors, waterfront, condition, sqft_basement, yr_built, yr_renovated,lot_log):
    """Takes inputs and uses city selection to index models pickle and predict house price.
    
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
        price {str}-- Formatted dollar amount of predicted house price.
    """
  
    model = model[int(city)]
    lot_log = np.log(int(lot_log))
    # Create of row of data that comabines all user inputs
    title={"bedrooms":[bedrooms], "bathrooms":[bathrooms], "floors":[floors], "waterfront": [waterfront], "condition":[condition], "sqft_basement":[sqft_basement],"yr_built":[yr_built], "yr_renovated":[yr_renovated], "lot_log":[lot_log]}
    test = pd.DataFrame(title)


    # Make prediction from the loaded random forest model
    prediction = model.predict(test)
    result = int(np.exp(prediction))
    price = '${:0,.0f}'.format(result)
    return price

