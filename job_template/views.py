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
    {'id': 1, 'title':'Template 1'},
    {'id': 2, 'title': 'Template 2'},
    {'id' : 3, 'title':'Template 3'}
    ]
    return render_template('job-template/templates.html', title='Templates', user=user, templates=templates)
