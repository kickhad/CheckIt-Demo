import os

from .settings import get_settings

# from dotenv import load_dotenv
# from .settings import settings
basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, ".env"))

class Config(object):
    TEMPDIR = r'C:\prod\prod01\app1\logs\dumps'
    DEBUG = True
    OFFLINE = True
    SECRET_KEY =  "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = r'mssql+pyodbc://flix:mitchell@DESKTOP-UUGSKQG\SQLEXPRESS/checkit?driver=SQL+Server+Native+Client+11.0'                              
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    suppress_callback_exceptions = True
    FLASK_ADMIN_SWATCH = 'cerulean'
    SETTINGS = {
    
    
    
    
'CURRENT_MY_WEEK':201924,
'TIMESTAMP_RECENT_EDI_TX':20190902,
'CURRENT_END_WEEK': 201952



} #get_settings(SQLALCHEMY_DATABASE_URI)
