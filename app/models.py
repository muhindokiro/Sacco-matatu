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
    route = db.relationship("Trips",backref = "assets",lazy = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    
    
    def save_asset(self):
        db.session.add(self)



        db.session.commit()


class Staffs(UserMixin, db.Model):
    """
    Create an staff table
    """
    __tablename__ = 'staffs'
   
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255),index = True)
    phone = db.Column(db.Integer,unique = True)
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime,default=datetime.now)
    staff_no = db.Column(db.Integer,unique = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin =db.Column(db.Boolean, default=False)
    
    def save_staff(self):
        db.session.add(self)
        db.session.commit()
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
       
         return check_password_hash(self.password_hash,password)
 
    def __repr__(self):
        return 'Staffs{self.name}'
 



class Trips(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.Integer, db.ForeignKey('assets.id'))
    route = db.Column(db.String(255),index = True)
    passengers = db.Column(db.Integer,unique = True)
    fare = db.Column(db.String(10),unique = True)
    station = db.Column(db.String(255),index = True)
    time = db.Column(db.DateTime,default=datetime.now)
    driver = db.Column(db.String(70),index = True)
    conductor = db.Column(db.String(70),index = True)




class Roles(db.Model):
    """
    Create a Role table
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    staff = db.relationship('Staffs', backref='roles',
                                lazy='dynamic')
   
    def __repr__(self):
 


        return 'Role{self.name}'
class Controller(ModelView):
    def is_accessible(self):
        if  current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(403)
   
    def not_auth(self):
        return "you are not authorised"


    
admin.add_view(ModelView(Owners, db.session))
admin.add_view(ModelView(Staffs, db.session))
admin.add_view(ModelView(Roles, db.session))
admin.add_view(ModelView(Assets, db.session))
admin.add_view(ModelView(Trips, db.session))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))