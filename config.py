import os
# from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    DEBUG = True
    OFFLINE = True
    SECRET_KEY =  "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = r'mssql+pymssql://DESKTOP-UUGSKQG\SQLEXPRESS\checkit'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    suppress_callback_exceptions = True
    FLASK_ADMIN_SWATCH = 'yeti'
