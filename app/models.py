import os
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db,login_manager,admin
from datetime import datetime
from flask_login import login_required,current_user
from flask import render_template,request,redirect,url_for,abort
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

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
    asset = db.relationship('Assets', backref='owner', lazy=True)

  

    # def __init__(self, name, email, phone,asset, date_added):
    #     self.name = name
    #     self.email = email
    #     self.phone = phone
    #     self.asset = asset
    #     self.date_added = date_added
   
  
    def save_owner(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f' {self.name}'

class Assets(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.String(10), index=True)
    route = db.relationship("Routes",backref = "asset",lazy = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))

    
    # def __init__(self,number_plate,route,owner_id):
    #     self.number_plate = number_plate
    #     self.route = route
    #     self.owner_id = owner_id

    @classmethod
    def get_assets(cls):
        assets = Assets.query.order_by('id').all()      
        return assets
    
    @classmethod
    def get_asset(cls,id):
        asset = Assets.query.filter_by(id=id).first()
        return asset 


    def __repr__(self):
        return f' {self.number_plate}'
    
    # def save_asset(self):
    #     db.session.add(self)
    #     db.session.commit()


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
    is_admin =db.Column(db.Boolean, default=False)
    
    def save_staff(self):
        db.session.add(self)
        db.session.commit()
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer('SECRET_KEY', expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s=Serializer('SECRET_KEY')
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Staffs.query.get(user_id)
    



    # def __init__(self,name,phone,email,password_hash,staff_no, date_added,is_admin):
    #     self.name = name
    #     self.phone = phone
    #     self.email = email
    #     self.password_hash = password_hash
    #     self.staff_no = staff_no
    #     self.date_added = date_added
    #     self.is_admin = is_admin


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
       
        return check_password_hash(self.password_hash,password)
 

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


 
        


class Routes(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.Integer, db.ForeignKey('assets.id'))
    staff_name = db.Column(db.String(255),index = True)
    driver = db.Column(db.String(255),index = True)
    conductor = db.Column(db.String(255),index = True)
    route = db.Column(db.String(255),index = True)
    passengers = db.Column(db.Integer,unique = True)
    fare = db.Column(db.String(10),unique = True)
    station = db.Column(db.String(255),index = True)
    time = db.Column(db.DateTime,default=datetime.now)

    # def __init__(self, number_plate,staff_name, driver, conductor, route, passengers, fare, station, time):
    #     self.number_plate = number_plate
    #     self.staff_name = staff_name
    #     self.driver = driver
    #     self.conductor = conductor
    #     self.route = route
    #     self.passengers = passengers
    #     self.fare = fare
    #     self.station = station
    #     self.time = time
    @classmethod
    def get_routes(cls, id):
        routes = Routes.query.order_by(number_plate=id).desc().all()
        return routes
    def __repr__(self):

        return f' {self.route}'

class Controller(ModelView):
    def is_accessible(self):
        if  current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(403)

    def not_auth(self):
        return "you are not authorised"
    



admin.add_view(Controller(Owners, db.session))
admin.add_view(Controller(Staffs, db.session))
admin.add_view(Controller(Assets, db.session))
admin.add_view(Controller(Routes, db.session))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

