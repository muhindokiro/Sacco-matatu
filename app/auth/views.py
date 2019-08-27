from flask import render_template,redirect,url_for,flash,request
from . import auth
from ..models import Owners, Assets, Staffs, Routes
from .forms import LoginForm,RegistrationForm,AdminForm,RequestResetForm,PasswordResetForm
from .. import db,mail
from flask_login import login_user,logout_user,login_required,current_user
from ..email import mail_message
from flask_mail import Message

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

def send_reset_email(staff):
    token = staff.get_reset_token()
    msg = Message('password reset request', sender = "juniormango2015@gmail.com", recipients=[staff.email])
    msg.body =f"""visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)
    

@auth.route('/reset_password',methods = ['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        staff = Staffs.query.filter_by(email=form.email.data).first()
        send_reset_email(staff)
        flash('an email has been send with instruction to reset the password.', 'info')
        
    return render_template('auth/request_reset.html', title = "reset password",request_form=form)


@auth.route('/reset_password/<token>',methods = ['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    staff=Staffs.verify_reset_token(token)
    if staff is None:
        flash('that is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = PasswordResetForm
    return render_template('auth/reset_token.html', title = "reset password",form=form)
