from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from ..models import Staffs, Role, Department


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class StaffAssignForm(FlaskForm):
    """
    Form for admin to roles to staffs
    """
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    submit = SubmitField('Submit')
