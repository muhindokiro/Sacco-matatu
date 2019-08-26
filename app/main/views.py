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



