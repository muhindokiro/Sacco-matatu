import os

class Config:

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2:'
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'abcdef'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #     email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'thefirifo@gmail.com'
    MAIL_PASSWORD = '4a2812336'
    
   
    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    pass

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://phirifo:1234@localhost/sacco_test'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://phirifo:1234@localhost/saccoadmintest2'
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}


# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://phirifo:1234@localhost/sacco2'

# class DevConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://phirifo:1234@localhost/saccoadmintest