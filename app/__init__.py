import os
from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)
mail = Mail()
admin = Admin(name='Sacco-admin',template_mode="bootstrap3")

def create_app(config_name):

    app = Flask(__name__)
    # Creating the app   configurations
    app.config.from_object(config_options[config_name])
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

    # Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    

    # Registering the blueprint
    #from .admin import admin as admin_blueprint
    #app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/authenticate')

    # configure UploadSet
    configure_uploads(app, photos)
    
    
    
    

    return app
