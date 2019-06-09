
# AVC Project repository
## Creator: Tova Simonson
## QA: Molly Srour
<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
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



## Repo structure 

```
├── README.md                         <- You are here
│
├── static                            <- Directory for CSS, images that remain static 
│   ├── about.png/                    <- Image for 'about' header.
│   ├── banner4.png/                  <- Image for 'homepage' header.
│   ├── basic.css/                    <- CSS for all html templates.
│   ├── contact.png/                  <- Image for 'contact' header.
│   ├── data.png/                     <- Image for 'data' header.
│   ├── decrease.png/                 <- Image icon for price decrease on results page.
│   ├── house.png/                    <- Image icon for home price prediction on results page.
│   ├── result_banner1.png/           <- Image for 'result' page header.
|
├── templates/                        <- Directory for HTML that is templated and changes based on a set of inputs
│   ├── about.html/                   <- Template for about page.
│   ├── contact.html/                 <- Template for contact page.
│   ├── data.html/                    <- Template for data page.
│   ├── index.html/                   <- Template for home page.
│   ├── result.html/                  <- Template for result page.
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── config.yml/                   <- Configuration yaml file for getting data and training model.
|   ├── fask_config.py/               <- Configuration file for flask app. 
│
├── data                              <- Folder that contains data used or generated. 
│
├── Seattle Models.ipynb              <- Original notebook used for EDA, training, building out logic. 
│
├── acquire_data.py                   <- Script for taking raw data in S3 bucket and moving to personal bucket.
├── db2.py                            <- Script for setting up database for user input (SQLite or RDS)
├── make_data.py                      <- Script for setting up features and data for model, configured by config.yml
├── train_data.py                     <- Script for training and scoring models, configured by config.yml
├── application.py                    <- Script for running the application
├── predict.py                        <- Script for predicting price to be used in application.
├── decrease_price.py                 <- Script for finding price decrease to be used in application.
├── unit_tests.py                     <- Script for testing functions working correctly before and after application set up.
├── makefile                          <- File to link together and create necessary files, models, etc. 
├── config_db.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).
The HTML/CSS menu was found at https://codepen.io/animatedcreativity/pen/wOqBQr by "Animated Creativity" on codepen (https://codepen.io/animatedcreativity/pens/popular/). 

## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. Please be in the directory of this project before installing `requirements.txt`.

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv housingApp

source housingApp/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n housingApp python=3.7
conda activate housingApp
pip install -r requirements.txt

```

### 2. Set up configurations for RDS (database) and AWS (get data):

`config_db.py` holds the configurations. It includes the following configurations:

MYSQL_USER=""

MYSQL_PASSWORD=""

MYSQL_HOST=""

MYSQL_PORT=""

DATABASE_NAME=""

AWS_KEY_ID=""

AWS_ACCESS_KEY=""

AWS_BUCKET=""

AWS_FILE_PATH=""



### 3. Get the data

To put the data into your S3 Bucket that was configured in `config_db.py`, run:
```
python acquire_data.py
```
Note: if you are not using the default "data" folder please make your directory folder before running the above line by running `mkdir folder`
 
 

### 4. Initialize the database 

To create the empty database in RDS, configured in `config_db.py`, run: 

```
python db2.py --rds=True
```

To create a SQLite database, with default name (user.db) run:

```
python db2.py 
```

To create a SQLite database, with different name (name in format with db extension like name.db) run:

```
python db2.py --dbName=name.db
```

### 5. Run data generation and training

If using default settings(for input/output/config paths), to generate features, train, and score model, run:

```
make all
```
If you do not want to use default settings, the data is created and the model is trained using a makefile. Edit the `makefile` to change input, output, and config paths. To change attributes of the model and paths for getting data and training, edit `config.yml`. If your path is not in a  `data` folder, please create whichever folder you would like to use by doing `mkdir folder`.

To edit these files: 
```
vi makefile
```
```
vi config/config.yml
```

Run generating and training:
```
make all
```


### 6. Application

When the application runs, it uses models saved from part 5.


To run the application, using SQLite database, with the default (data/model.pkl) model file, run:

```
python application.py
```

To run the application, unsing SQLite database, with a different model path, run:

```
python application.py --input=your_model_path
```

To run the application, using RDS, uncomment MYSQL specifications in `config/flask_config.py`, fill in your information:
```
vi config/flask_config.py
```
Then comment out the old SQLALCHEMY_DATABASE_URI. And run as instructed before. 



## Testing
In order to run testing on the application, run:
```
py.test
```

