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

from flask_weasyprint import HTML, render_pdf

from flask_mail import Message
from . import mail
from .email import mail_message


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
    trip = db.relationship('Trips', backref='owners', lazy=True)
   
  
    def save_owner(self):
        db.session.add(self)
        db.session.commit()
    

    def __repr__(self):
        return f' {self.name}'


class Assets(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.String(10), index=True)
    route = db.relationship("Trips",backref = "assets",lazy = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))

    def __repr__(self):
        return f' {self.number_plate}'
    
    
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
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id',ondelete='CASCADE'))
    is_admin =db.Column(db.Boolean, default=False)


    def __repr__(self):
        return f' {self.name}'
    
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
    staff_name = db.Column(db.String(70),index = True)
    route = db.Column(db.String(255),index = True)
    passengers = db.Column(db.Integer,index = True)
    fare = db.Column(db.String(10),index = True)
    station = db.Column(db.String(255),index = True)
    time = db.Column(db.DateTime,default=datetime.now)
    driver = db.Column(db.String(70),index = True)
    conductor = db.Column(db.String(70),index = True)
    trip_total_fare = db.Column(db.String(70),index = True)
    owner = db.Column(db.Integer, db.ForeignKey('owners.id'))

    

    # def __init__(self,route,passengers, fare, station, driver, conductor):
        
    #     self.route = route
    #     self.passengers = passengers
    #     self.fare = fare
    #     self.station = station
    #     self.driver = driver
    #     self.conductor = conductor


    def __repr__(self):
        return f' {self.number_plate}'

    def save_trip(self):
        db.session.add(self)
        db.session.commit()




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



class Controller(ModelView):
    def is_accessible(self):
        if  current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(403)
   
    def not_auth(self):
        return "you are not authorised"

class Mytools(ModelView):
    can_delete = True
    page_size = 50
    column_searchable_list = ['phone']


def action(name, text, confirmation=None):
    """
        Use this decorator to expose actions that span more than one
        entity (model, file, etc)

        :param name:
            Action name
        :param text:
            Action text.
        :param confirmation:
            Confirmation text. If not provided, action will be executed
            unconditionally.
    """
    def wrap(f):
        f._action = (name, text, confirmation)
        return f

    return wrap


class TheView(ModelView):

    @action('print summary', 'Print Summary', 'Are you sure you want to print summary?')
    def action_recalculate(self, ids):

        #trips = Trips.query.get(ids)
        #trips = Trips.query.all()
        trips = Trips.query.filter(Trips.id.in_(ids)).all()
        name = 'trips'
        ids = ids

        html = render_template('tripsreport.html', ids=ids, name=name, trips=trips)

        owneremail='';
        for singletrip in trips:
            owneremail = singletrip.owners.email;
            if owneremail != '':
                break


        mail_message("Trip report","email/trip_report",owneremail,ids=ids, name=name, trips=trips)


        return render_pdf(HTML(string=html))    
        # count = 0
        # for _id in ids:
        #     transaction_service.recalculate_transaction(_id)
        #     count += 1
        # flash("{0} transaction (s) charges recalculated".format(count))



    





admin.add_view(Mytools(Staffs, db.session))
    
admin.add_view(ModelView(Owners, db.session))
# admin.add_view(ModelView(Staffs, db.session))
# admin.add_view(ModelView(Roles, db.session))
admin.add_view(ModelView(Assets, db.session))
admin.add_view(TheView(Trips, db.session))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
