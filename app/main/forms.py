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


class OwnersForm(FlaskForm):

    name = StringField('Full Name',validators=[Required()])
    email = StringField('Email',validators=[Required()])
    phone = StringField('Phone', validators=[Required()])
    submit = SubmitField('Submit')


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




# class OwnersForm(ModelForm, FlaskForm):
#     class Meta:
#         model = Owners



# class AssetsForm(ModelForm, FlaskForm):
#     class Meta:
#         model = Assets
#     owner = ModelFieldList(FormField(OwnersForm))





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





# class Trips(db.Model):
#     __tablename__ = 'routes'
#     id = db.Column(db.Integer, primary_key=True)
#     number_plate = db.Column(db.Integer, db.ForeignKey('assets.id'))
#     route = db.Column(db.String(255),index = True)
#     passengers = db.Column(db.Integer,unique = True)
#     fare = db.Column(db.String(10),unique = True)
#     station = db.Column(db.String(255),index = True)
#     time = db.Column(db.DateTime,default=datetime.now)