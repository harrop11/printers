import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bkk'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    IMAGE_UPLOAD = "/home/lnvd/projects/py/bkk/app/static/img"
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'ebkk.db')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root@127.0.0.1/print'
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'ebkk.db')
    TESTING = True
