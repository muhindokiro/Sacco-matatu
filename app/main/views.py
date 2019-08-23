from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Owners, Assets, Staffs, Routes
from .forms import OwnerForm,UpdateProfile
from flask_login import login_required,current_user
from .. import db,photos


#comment
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home'
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