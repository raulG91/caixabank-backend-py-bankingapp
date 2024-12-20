import os
class Config(object):
    SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    JWT_SECRET = '40a9914ca0dab6c28e25205404a8b74a6f7414e91d7be81a5692f54b612f89d4d4c79223f04a2e67efd5c37925f6cbc88d245edbf8e5fd1abc36cf0ad6ee33a3f596de9978d25f5502c0f249ca2dd7907d600505a3519500939529d544590c7634dd38b61dc7909fc1dc1404ea3b0e085e17bc7164be7d52fb799fed2146917c'
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
