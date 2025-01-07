import os
class Config(object):
    SECRET_KEY = 'Your key'
    JWT_SECRET = 'Your JWT Key'
    JWT_TOKEN_LOCATION = ['headers']
    MAIL_USE_TLS = True       # No encryption needed for local testing
    MAIL_USE_SSL = False
    MAIL_USERNAME = None       # No authentication required
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = 'no-reply@test.com'
    MAIL_DEBUG = False  # Explicitly set MAIL_DEBUG
    MAIL_SUPPRESS_SEND = False
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/bankingapp'
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    MAIL_SERVER = '172.17.0.2'
    MAIL_PORT = 1025
 

class ProdConfig(Config):
    
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = os.environ['MAIL_PORT']
