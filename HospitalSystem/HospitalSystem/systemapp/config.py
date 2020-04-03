import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you never know'

    SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' +os.path.join(basedir,'systemdb.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PIC_UPLOAD_DIR = os.path.join(basedir,'images')