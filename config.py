import os

"""
different classes for different configurations allows us to use environment variables based on 
the environment - local, staging, production, etc
"""

#returns directory name where this file (script) is located. 
#If directory structure changes, basedir will change as well. abspath 'Return a normalized absolutized version of the pathname path.'
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    # The secret key is needed to keep the client-side sessions secure. (Unique to app)
    # SECRET KEY NEEDS TO BE HIDDEN USING ENV VARIABLE BEFORE PRODUCTION
    SECRET_KEY = b'\x95\x87\x1c\xb7F\xeb\x03\xdd\xb5\xfa+\xb8:5\xcci\xff\xc9\tg>\xb5%\xaf'

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

