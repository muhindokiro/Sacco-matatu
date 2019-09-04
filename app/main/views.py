from flask import render_template,request,redirect,url_for,abort, jsonify
from . import main
from ..models import Owners, Assets, Staffs, Trips
from .forms import AssetsForm, RoutesForm
from flask_login import login_required
from .. import db,photos


# from flask_admin.contrib.sqla import ModelView

# from wtforms.ext.sqlalchemy import QuerySelectField

from flask_weasyprint import HTML, render_pdf


# @main.route('/hello/', defaults={'name': 'World'})
# @main.route('/hello/<name>/')
# def hello_html(name):
#     return render_template('hello.html', name=name)


@main.route('/hello_<name>.pdf')
def hello_pdf(name):
    # Make a PDF straight from HTML in a string.
    html = render_template('hello.html', name=name)
    return render_pdf(HTML(string=html))
    #return render_pdf(url_for('main.hello_html', name=name))




@main.route('/', methods = ['GET','POST'])
def index():

    
    title = 'Home'
    name = 'phil';
    return render_template('index.html',title = title, name = name)




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



# class RoutesForm(form.Form):
#     fare = fields.TextField('Fare')    
#     number_plate = QuerySelectField('Assets')




# @main.route('/trip', methods = ['GET','POST'])
# class RoutesView(ModelView):

#     def create_form(self):
#         form = RoutesForm()
#         form.assets.query = Assets.query.all()
#         return form





@main.route('/all_routes')
def listRoutes():
    routez = Trips.query.all()
    return render_template('all_trips.html', myRoutez=routez)



# @main.route('/asset_routes')
# def assetRoutes(number_plate):
#     aroutez = Trips.query.filter_by(number_plate=number_plate).first()
#     return render_template('asset_routes.html', aRoutez=aroutez)


@main.route('/apitest/felipe', methods = ['GET','POST'])
def philapi():
    
    if (request.method == 'POST'):
        phil_son = request.get_json()
        return jsonify({'hambari ngani' : phil_son}), 201
    else:
        return jsonify({'about' : 'hellow world'})
    








