# 2020-09-19 14:02:51 -0700 - Emily Martens - add more views to job_template bp, add task detail html page. - lines:,25,31,33,34,35,36,37,38,39,40,41,42,43
# 2020-09-19 13:07:50 -0700 - Emily Martens - add front end setup, blueprint setup for user, job_template - lines:,9,10,11,12,13,14,15,16,17,18,19,23,24
# 2020-09-19 16:30:14 -0700 - Emily Martens - add task blueprint with routes to task detail - lines:,20,21,22
# 2020-09-19 19:02:54 -0700 - Emily Martens - add views and navigation for add template, add task, and archive. - lines:,26,27,28,29,30
# 2020-09-23 23:09:41 -0400 - Jeremy Axmacher - Team collaborated on model schema definition - lines:,8
# 2020-09-19 19:46:10 -0700 - Emily Martens - add snooze and delete views, update styles - lines:,7,32,44,45,46,47,48,49,50,51,52,53,54,55,56
from flask import Blueprint, render_template, redirect, url_for, flash
from tasker.models import db
#from tasker.job_template.forms import JobTemplateForm

bp = Blueprint('job_template', __name__, static_folder='../static')

@bp.route('/templates')
#@login_required
def templates():
    user = {
    'username': 'test@testing.com', 'email' : 'test@testing.com', 'timezone' : 'EST', 'view' : 'Month'
    }
    templates = [
    {'id': 0, 'title':'Template 1', 'start_date' : '09.10.2020', 'interval': 3, 'interval_type' : 'Weeks', 'description' : 'Job Template description goes here.'},
    {'id': 1, 'title': 'Template 2', 'start_date' : '09.15.2020', 'interval': 5, 'interval_type' : 'Days', 'description' : 'Job Template description goes here.'},
    {'id' : 2, 'title':'Template 3', 'start_date' : '09.20.2020', 'interval' : 1, 'interval_type' : 'Months', 'description' : 'Job Template description goes here.'}
    ]
    return render_template('job-template/templates.html', title='Templates', user=user, templates=templates)

@bp.route('/add_template')
#@login_required
def add_template():
    return render_template('job-template/add-template.html', title="Create Template")

@bp.route('/template_detail/<id>')
#@login_required
def template_detail(id):
    user = {
    'username': 'test@testing.com', 'email' : 'test@testing.com', 'timezone' : 'EST', 'view' : 'Month'
    }
    templates = [
    {'id': 0, 'title':'Template 1', 'start_date' : '09.10.2020', 'interval': 3, 'interval_type' : 'Weeks', 'description' : 'Job Template description goes here.'},
    {'id': 1, 'title': 'Template 2', 'start_date' : '09.15.2020', 'interval': 5, 'interval_type' : 'Days', 'description' : 'Job Template description goes here.'},
    {'id' : 2, 'title':'Template 3', 'start_date' : '09.20.2020', 'interval' : 1, 'interval_type' : 'Months', 'description' : 'Job Template description goes here.'}
    ]
    template = templates[int(id)]
    return render_template('job-template/template-detail.html', title='Template Details', user=user, template=template)

@bp.route('/edit_template/<id>')
#@login_required
def edit_template(id):
    id = id
    return render_template('job-template/edit-template.html', title="Edit Template", id=id)

@bp.route('/delete_template/<id>')
#@login_required
def delete_template(id):
    id=id
    flash("Template deleted")
    return redirect(url_for('job_template.templates'))
