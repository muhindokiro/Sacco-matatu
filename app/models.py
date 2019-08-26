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

@login_manager.user_loader
def load_user(user_id):
    return Staffs.query.get(int(user_id))

class Owners(UserMixin, db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    phone = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(255), unique=True, index=True)
    date_added = db.Column(db.DateTime, default=datetime.now)
    asset = db.relationship('Assets', backref='owners', lazy=True)
   
  
    def save_user(self):
        db.session.add(self)
        db.session.commit()
    def __repr__(self):
        return f'Owners {self.name}'

class Assets(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.String(10), index=True)
    route = db.relationship("Routes",backref = "assets",lazy = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    
    
    def save_asset(self):
        db.session.add(self)
        db.session.commit()