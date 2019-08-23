
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from ..models import Department, Staffs, Role
from . import admin
from .forms import StaffAssignForm, RoleForm,DepartmentForm
from .. import db



def check_admin():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)
        
@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")
    
@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            db.session.rollback()
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")
    
    
@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            db.session.rollback()
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')
    
@admin.route('/staffs')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    staffs = Staffs.query.all()
    return render_template('admin/staffs/staffs.html',
                           staffs=staffs, title='Staff')
                           

@admin.route('/staffs/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    staff = Staffs.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if staff.is_admin:
        abort(403)

    form = StaffAssignForm(obj=staff)
    if form.validate_on_submit():
        staff.department = form.department.data
        staff.role = form.role.data
        db.session.add(staff)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_staffs'))

    return render_template('admin/staffs/staffs.html',
                          staff=staff, form=form,
                           title='Assign Staff')