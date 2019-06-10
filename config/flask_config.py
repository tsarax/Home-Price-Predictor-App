PORT = 3000
APP_NAME = "housing"
#check if name matches below
SQLALCHEMY_DATABASE_URI = 'sqlite:///user.db'  #comment out if using RDS
HOST = "0.0.0.0"

#UNCOMMENT OUT THE FOLLOWING IF USING RDS FOR DATABASE, THEN COMMENT OUT ABOVE URI
#conn_type = "mysql+pymysql"
#user = "MSQL_USER"
#password = "MYSQL_PASSWORD"
#host = "MYSQL_HOST"
#port = "MYSQL_PORT"
#DATABASE_NAME = 'msia423'
#SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".\
#format(conn_type, user, password, host, port, DATABASE_NAME)
