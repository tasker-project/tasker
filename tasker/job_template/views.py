from flask import Blueprint, render_template, redirect, url_for, flash
from tasker.models import db
#from tasker.job_template.forms import JobTemplateForm
from tasker.models import JobTemplate

bp = Blueprint('job_template', __name__, static_folder='../static')

@bp.route('/templates')
#@login_required
def templates():
    user = {
    'username': 'test@testing.com', 'email' : 'test@testing.com', 'timezone' : 'EST', 'view' : 'Month'
    }
    #templates = [
    #{'id': 0, 'title':'Template 1', 'start_date' : '09.10.2020', 'interval': 3, 'interval_type' : 'Weeks', 'description' : 'Job Template description goes here.'},
    #{'id': 1, 'title': 'Template 2', 'start_date' : '09.15.2020', 'interval': 5, 'interval_type' : 'Days', 'description' : 'Job Template description goes here.'},
    #{'id' : 2, 'title':'Template 3', 'start_date' : '09.20.2020', 'interval' : 1, 'interval_type' : 'Months', 'description' : 'Job Template description goes here.'}
    #]

    jobs = JobTemplate.getJobTemplates()
    for job in jobs:
        print("## name = " + job.name)
    #job = JobTemplate()
    #jobs = job.getJobTemplates()

    return render_template('job-template/templates.html', title='Templates', user=user, jobs=jobs)

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
