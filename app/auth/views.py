from flask import render_template,redirect,url_for,flash,request
from . import auth
from ..models import Owners, Assets, Staffs, Routes
from .forms import LoginForm,RegistrationForm,AdminForm,RequestResetForm,PasswordResetForm
from .. import db
from flask_login import login_user,logout_user,login_required
from ..email import mail_message

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        staff = Staffs.query.filter_by(email = login_form.email.data).first()
        if staff is not None and staff.verify_password(login_form.password.data):
            login_user(staff,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid Username or Password')

    title = "staff login"
    return render_template('auth/login.html',login_form = login_form,title=title)


@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        staff = Staffs(email = form.email.data, name = form.name.data,password = form.password.data)
         
        session['anonymous_user_id'] = staff.id
        db.session.add(staff)
        db.session.commit()

        return redirect(url_for('auth.login'))
    title = "New Account"
    return render_template('auth/register.html',registration_form = form, title=title)

@auth.route('/create_admin',methods = ["GET","POST"])
def create_admin():
    # prevent non-admins from accessing the page
    form = AdminForm()
    if form.validate_on_submit():
        staff = Staffs(email = form.email.data, name = form.name.data,password = form.password.data,is_admin = True )
        db.session.add(staff)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('auth/admin_signup.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out')
    return redirect(url_for("main.index"))
