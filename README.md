#for midproject
To grab data from my S3 bucket and put to your own:
-edit the config.py file and input AWS_KEY_ID, AWS_ACCESS_KEY, AWS_BUCKET, and AWS_FILE_PATH. 

In order to make database in RDS: 
-edit the config.py file and input RDS credentials: MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT

# Example project repository

<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
    + [With `conda`](#with-conda)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Initialize the database](#3-initialize-the-database)
  * [4. Run the application](#4-run-the-application)
- [Testing](#testing)

<!-- tocstop -->

## Project Charter 

**Vision**: The 2018 National Association of Realtors Profile of Home Buyers and Sellers indicate that 50% of home buyers find the home they purchase on the internet. While the internet enables consumers to gather greater information regarding such an important decision, starting a search to find a home can be daunting. With this app, potential buyers in King County, USA will have a place to easily find a price approximation for their dream home and see how changes in home attributes can make their search more affordable and realistic, allowing them to narrow their search and make the process less daunting. This can be quite impactful because King County is home to approximately 2.189 million residents, including the major city of Seattle and surrounding areas. 

**Mission**: The app will allow a user to input criteria they are interested in for a home purchase in King County, such as bedroom and bathroom count, square footage, waterfront access, condition, year built range, and approximate zipcode or city name. The user will then receive a prediction of cost for a home with those attributes and suggest the best cost saving attribute to give up. For instance, if bathroom count would significantly decrease the predicted cost of the home the most out of any attribute, this attribute would be suggested to change.

**Success criteria**: In order to evaluate the success of the project, we will produce metrics for the performance of our model by splitting the dataset into test and train sets and calculate predictions. The main performance metric will be test R^2 since this value will also indicate the lowest RMSE, which is the root mean squared error between the predictions and the actual values. Anything above a 50% R^2 will indicate a success. If the R^2 is above this criteria, it indicates the predictions for house prices match closely to the actual observed prices. 
As our mission is to make the house hunting process less daunting, faster, and more affordable, the business success will be determined by user appreciation for suggestions given by the app. For instance, once a user runs their search in the app, we will give the predicted cost and a suggestion for changing an attribute that reduces this cost. The user can interact with the interface to indicate if this suggestion was helpful or not. 


## Backlog 
\* indicates to-do in next two weeks

### Theme1: Predicting Housing Cost

***Epic1:*** Python-Based Predictive Model

**Story1:** Data Cleaning - 2points 

**Story2:** Model Building: Stepwise Linear Regression -1 point 

**Story3:** Model Predictions: Linear Regression -1 point 

**Story4:** Model Building: Random Forest -1 point 

**Story5:** Model Predictions: Random Forest -1 point 

**Story6:** Compare Models & Pick Best - 0 points 

**Story7:** Model Testing -2 points 

**Story8:** Model Unit Testing -4 points \*

**Story9:** Model Scripts - 4 points \*

**Story10:** Model documentation - 4 points \*

***Epic2:*** Data Setup

**Story1:** S3 raw data - 1 point \*

**Story2:** RDS set up and script - 1 point \*

***Epic3:*** User Interface

**Story1:** Develop interface code (CSS and HTML) -8 points

**Story2:** User input interact with model -4 points

**Story3:** A/B Testing -8 points

### Theme2: Housing Scenario Generator

***Epic1:*** Predict most significant attribute to decrease cost

**Story1:** Develop code to indicate most significant price change -4 points

**Story2:** Develop code to change the significant attribute appropriately and run a new prediction -4 points

***Epic2:*** User Interface

**Story1:** Develop interface code for showing suggestion -2 points

**Story2:** Develop two buttons: like and dislike for suggestion-4 points

**Story3:** Store suggestion likes and dislikes -4 points

**Stroy4:** Logging Information -4 points


## Icebox

### Theme1: Compare Searches

***Epic1:*** Storing past search and result

**Story1:** Create dataframe for searches done during session -8 points

***Epic2:*** Changing interface for new search

**Story1:** Create button for new search -2 points

**Story2:** Move past search below current search -8 points


## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│   ├── archive                       <- No longer current models. This directory is included in the .gitignore and is not tracked by git
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports and helper functions. 
│
├── src                               <- Source data for the project 
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── add_songs.py                  <- Script for creating a (temporary) MySQL database and adding songs to it 
│   ├── ingest_data.py                <- Script for ingesting data from different sources 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── postprocess.py                <- Script for postprocessing predictions and model results
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── test                              <- Files necessary for running model tests (see documentation below) 

├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. See bottom of README for exploratory data analysis environment setup. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv pennylane

source pennylane/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n pennylane python=3.7
conda activate pennylane
pip install -r requirements.txt

```

### 2. Configure Flask app 

`config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
PORT = 3002  # What port to expose app on 
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tracks.db'  # URI for database that contains tracks

```


### 3. Initialize the database 

To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

To add additional songs:

`python run.py ingest --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`


### 4. Run the application 
 
 ```bash
 python app.py 
 ```

### 5. Interact with the application 

Go to [http://127.0.0.1:3000/]( http://127.0.0.1:3000/) to interact with the current version of hte app. 

## Testing 

Run `pytest` from the command line in the main project repository. 


Tests exist in `test/test_helpers.py`
