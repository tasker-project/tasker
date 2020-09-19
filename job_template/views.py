from flask import Blueprint, render_template
from tasker.database import db
#from tasker.job_template.forms import JobTemplateForm

bp = Blueprint('job_template', __name__, static_folder='../static')

@bp.route('/templates')
#@login_required
def templates():
    user = {
    'username': 'test@testing.com', 'email' : 'test@testing.com', 'timezone' : 'EST', 'view' : 'Month'
    }
    templates = [
    {'id': 0, 'title':'Template 1'},
    {'id': 1, 'title': 'Template 2'},
    {'id' : 2, 'title':'Template 3'}
    ]
    return render_template('job-template/templates.html', title='Templates', user=user, templates=templates)

@bp.route('/template_detail/<id>')
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
