from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Owners, Assets, Staffs, Routes,Roles
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


@main.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('dashboard.html', title="Dashboard")


@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('admin_dashboard.html', title="Dashboard")

class Controller(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def not_auth(self):
        return "you are not authorised"