import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1KOCWnVTb0fPb0EQgyDhAbk8TJPs1Q9LhbsfeEc2fLVxa2ncBT6AfIWdpnwjbhan9lmix0iR2yxyvMEfRaMl0oyrzLjykizMRlt5'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Maks13245612@127.0.0.1:3306/kursach'
    SQLALCHEMY_TRACK_MODIFICATION = False

class DevelopmentConfig(Config):
    Debug = True

class ProductionConfig(Config):
    Debug = False