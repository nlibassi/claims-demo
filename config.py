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
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x95\x87\x1c\xb7F\xeb\x03\xdd\xb5\xfa+\xb8:5\xcci\xff\xc9\tg>\xb5%\xaf'
    # db url is also env-based
    #is app.db created in the background when the Flask app object is created? don't think so
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or 'postgresql:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #upload folder hardcoded for now in routes, change later
    #UPLOAD_FOLDER = os.path.basename('/home/nlibassi/claims-demo-uploads')
    #add security salt later
    #SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    #SECURITY_PASSWORD_SALT = 

    """
    finish later
    SECURITY_EMAIL_SENDER = 'no-reply@example.com'
    MAIL_SERVER = 'email-smtp.us-west-2.amazonaws.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    """

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

