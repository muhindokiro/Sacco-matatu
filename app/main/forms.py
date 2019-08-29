from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required
from wtforms_alchemy import ModelForm, ModelFieldList
from ..models import Owners, Assets, Trips



from flask_wtf import Form
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.orm import model_form
from .. import db

from wtforms.fields import FormField




# class AssetsForm(FlaskForm):

#     number_plate = StringField('Number Plate',validators=[Required()])
#     trip_details = StringField('Trip',validators=[Required()])
#     owner_id = StringField('Owner', validators=[Required()])
#     submit = SubmitField('Submit')



exclude_properties = ['trip_details']
AssetsForm = model_form(model=Assets,
        base_class=Form,
        db_session=db.session,
        exclude=exclude_properties)
AssetsForm.submit = SubmitField('Create')










# class RoutesForm(FlaskForm):

#     # number_plate = StringField('Number Plate',validators=[Required()])
#     route = StringField('Route',validators=[Required()])
#     passengers = StringField('Passengers', validators=[Required()])
#     fare = StringField('Fare',validators=[Required()])
#     station = StringField('Station',validators=[Required()])
#     driver = StringField('Driver',validators=[Required()])
#     conductor = StringField('Conductor',validators=[Required()])
#     submit = SubmitField('Submit')


exclude_properties = ['time']
RoutesForm = model_form(model=Trips,
        base_class=Form,
        db_session=db.session,
        exclude=exclude_properties)
RoutesForm.submit = SubmitField('Create')




# from wtforms.ext.sqlalchemy import QuerySelectField

# class RoutesForm(form.Form):
#     fare = fields.TextField('Fare')    
#     number_plate = QuerySelectField('Assets')

# class RoutesView(ModelView):

#     def create_form(self):
#         form = RoutesForm()
#         form.assets.query = Assets.query.all()
#         return form