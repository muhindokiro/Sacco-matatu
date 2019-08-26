from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager,admin
from datetime import datetime
from flask_login import login_required,current_user
from flask import render_template,request,redirect,url_for,abort
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op