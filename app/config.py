import os
class Config(object):
 
    JWT_TOKEN_LOCATION = ['headers']
    MAIL_USE_TLS = False       # No encryption needed for local testing
    MAIL_USE_SSL = False
    MAIL_USERNAME = None       # No authentication required
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = 'no-reply@example.com'
    MAIL_DEBUG = True  # Explicitly set MAIL_DEBUG
    MAIL_SUPPRESS_SEND = False
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/bankingapp'
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    MAIL_SERVER = '172.17.0.2'
    MAIL_PORT = 1025
 

class ProdConfig(Config):
    SECRET_KEY =  os.environ['SECRET_KEY']
    JWT_SECRET = os.environ['JWT_SECRET'] 
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = os.environ['MAIL_PORT']
