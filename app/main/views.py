from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Owners, Assets, Staffs, Trips
from .forms import OwnersForm, AssetsForm, RoutesForm
from flask_login import login_required
from .. import db,photos



#comment
@main.route('/', methods = ['GET','POST'])
def index():

    
    title = 'Home'
    return render_template('index.html',title = title)




@main.route('/trip', methods = ['GET','POST'])
def trip():

    routes_form = RoutesForm()
    

    if  routes_form.validate_on_submit():        
        route =  routes_form.route.data
        passengers =  routes_form.passengers.data
        fare =  routes_form.fare.data
        station =  routes_form.station.data
        driver =  routes_form.driver.data
        conductor =  routes_form.conductor.data
        # number_plate =  routes_form.number_plate.data
        index = Trips(route,passengers, fare, station, driver, conductor)
        index.save_trip()
        return redirect(url_for('main.trip'))
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Routes'
    return render_template('trip.html',title = title, routes_form = routes_form)








@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))