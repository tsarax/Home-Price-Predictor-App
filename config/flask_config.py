DEBUG = True
#LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "housing"
SQLALCHEMY_DATABASE_URI = 'sqlite:///user.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "8000"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

#UNCOMMENT OUT THE FOLLOWING IF USING RDS FOR DATABASE, THEN COMMENT OUT ABOVE URI
#conn_type = "mysql+pymysql"
#user = os.environ.get("MYSQL_USER")
#password = os.environ.get("MYSQL_PASSWORD")
#host = os.environ.get("MYSQL_HOST")
#port = os.environ.get("MYSQL_PORT")
#DATABASE_NAME = 'msia423'
#SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".\
#format(conn_type, user, password, host, port, DATABASE_NAME)
