from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Owners, Assets, Staffs, Routes, Roles
from .forms import OwnerForm,UpdateProfile
from flask_login import login_required,current_user
from .. import db,photos
from flask_admin.contrib.sqla import ModelView



#comment

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Sacco_Matatu_project'
    return render_template('index.html',title = title)


@main.route('/create_admin',methods = ["GET","POST"])
def create_admin():
    # prevent non-admins from accessing the page
    if request.method =="POST":
        new_staff = Staffs(email=request.form['email'],password=request.form['password'],is_admin = True )
        db.session.add(new_staff)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('auth/admin_signup.html')

