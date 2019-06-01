from flask import Flask, render_template, request, session, g, redirect, url_for, abort, render_template, flash
import os
from predict import prediction
from decrease_price import dec_price
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from db2 import User
import logging
import argparse
import pickle

logger = logging.getLogger(__name__)


app= Flask(__name__)

# config
app.config.from_object(__name__)

app.config.from_pyfile('config/flask_config.py')
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def mainpage():
    """Main page of the webapp
    Args:
        Null
    Returns:
        flask-obj: rendered html page
        
    """
    logger.info('At main app page.')
    return render_template('index.html')
 

@app.route('/results',methods=['POST'])
def result():
    """Result page of webapp
    Args:
        Null
    Returns:
        flask-obj: rendered html page
    """
    #sets user input of form equal to following variables
    logger.info("At results page.")
    user1 = request.form['city']
    user2 = request.form['bedrooms']
    user3 = request.form['bathrooms']
    user4 = request.form['floors']
    user5 = request.form['waterfront']
    user6 = request.form['condition']
    user7 = request.form['sqft_basement']
    user8 = request.form['yr_built']
    user9 = request.form['yr_renovated']
    user10 = request.form['lot_log']

    with open(path1, "rb") as f:
        models = pickle.load(f)


    logger.info('Got user input.')
    user_input1 = User(city=user1, bedrooms=user2, bathrooms=user3, floors=user4, waterfront=user5, condition=user6, sqft_basement=user7, yr_built=user8, yr_renovated=user9,lot_log=user10)
    db.session.add(user_input1)
    db.session.commit()
    logger.info("User input committed to database: %s, %s, %s, %s, %s, %s, %s, %s, %s, %s", user1, user2, user3, user4, user5, user6, user7, user8, user9, user10)

    # predict house price using model.prediction
    housepred= prediction(models, user1, user2, user3, user4, user5, user6, user7, user8, user9, user10)
    attribute_and_change, price_changes = dec_price(models, user1, user2, user3, user4, user5, user6, user7, user8, user9, user10)
    try:
        attribute = attribute_and_change[0]
        change = attribute_and_change[1]
        low_price = int(np.exp(min(price_changes)[0]))
        price = '${:0,.0f}'.format(low_price)
        if price == housepred:
            attribute=0
            change = 0
            price = 0
        logger.info("Sucessfully found if there was an attribute that could lower price.")
    except:
        attribute=0
        change = 0
        price = 0
        logger.warning("Could not find attribute change and lower price.")


    return render_template('result.html', result=housepred, result2=attribute, result3=change, result4=price)
   

@app.route('/about')
def about():
    """ View that renders pdf
    :return: Rendered html template
    """
    logger.info('User visited the about page.')
    return render_template('about.html')

@app.route('/data')
def data():
    """ View that renders pdf
    :return: Rendered html template
    """
    logger.info('User visited the data page.')
    return render_template('data.html')

@app.route('/contact')
def contact():
    """ View that renders pdf
    :return: Rendered html template
    """
    logger.info('User visited the contact page.')
    return render_template('contact.html')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict cloud class")
    parser.add_argument('--input', help='input path', default="data/model.pkl")
    args = parser.parse_args()
    path1 = args.input
    app.run(host = '0.0.0.0', use_reloader=True, port=3000)
