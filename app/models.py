
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager
from datetime import datetime



class Owners(UserMixin, db.Model):
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    phone = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))
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

class Staffs(UserMixin, db.Model):

    """
    Create an staff table
    """

    __tablename__ = 'staffs'
   
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255),index = True)
    phone = db.Column(db.Integer,unique = True)
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    date_added = db.Column(db.DateTime,default=datetime.now)
    staff_no = db.Column(db.Integer,unique = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def save_staff(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return 'Staffs{self.name}'
        
@login_manager.user_loader
def load_user(user_id):
    return Staffs.query.get(int(user_id))


class Routes(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.Integer, db.ForeignKey('assets.id'))
    route = db.Column(db.String(255),index = True)
    passengers = db.Column(db.Integer,unique = True)
    fare = db.Column(db.String(10),unique = True)
    station = db.Column(db.String(255),index = True)
    time = db.Column(db.DateTime,default=datetime.now)



class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    staff = db.relationship('Staffs', backref='department',
                                lazy='dynamic')
    def __repr__(self):
        return 'Department{self.name}'

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    owners = db.relationship('Staffs', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return 'Role{self.name}'
    
