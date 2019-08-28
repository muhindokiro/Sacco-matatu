import os

class Config:


    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://blaise:tribune@localhost/prodev'
    SECRET_KEY = 'matatu'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2:'

    UPLOADED_PHOTOS_DEST ='app/static/photos'
    

    #     email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    
   
    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    pass

class TestConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://blaise:tribune@localhost/prodev'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://blaise:tribune@localhost/prodev'

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mango:mango@localhost/sacco_test'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mango:mango@localhost/sacco_test'

    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}
