# 2020-09-19 18:16:30 -0700 - Emily Martens - add JS functionality, add change view front end controls and styles - lines:,4,6,10,12,32,33,34,35,36,37,38
# 2020-09-19 13:07:50 -0700 - Emily Martens - add front end setup, blueprint setup for user, job_template - lines:,5,7,8,9,11,13,14,15,16,17
# 2020-09-19 16:30:14 -0700 - Emily Martens - add task blueprint with routes to task detail - lines:,18,19,20,21,22,23,24,25,26,27,28,29,30,31
from flask import Blueprint, render_template, redirect, request, url_for
from tasker.database import db
from tasker.user.forms import ChangeViewForm

bp = Blueprint('user', __name__, static_folder='../static')

@bp.route('/', methods=['GET', 'POST'])

@bp.route('/home', methods=['GET', 'POST'])
#@login_required
def home():
    user = {
    'username': 'test@testing.com', 'email' : 'test@testing.com', 'timezone' : 'EST', 'view' : 'Month'
    }
    templates = [
    {'id': 0, 'title':'Template 1', 'start_date' : '09.10.2020', 'interval': 3, 'interval_type' : 'Weeks', 'description' : 'Job Template description goes here.'},
    {'id': 1, 'title': 'Template 2', 'start_date' : '09.15.2020', 'interval': 5, 'interval_type' : 'Days', 'description' : 'Job Template description goes here.'},
    {'id' : 2, 'title':'Template 3', 'start_date' : '09.20.2020', 'interval' : 1, 'interval_type' : 'Months', 'description' : 'Job Template description goes here.'}
    ]
    tasks = [
    {'id' : 0, 'due_date' : '9.10.2020', 'template': templates[0]},
    {'id' : 1, 'due_date' : '9.20.2020', 'template': templates[1]},
    {'id' : 2, 'due_date' : '9.25.2020', 'template': templates[1]},
    {'id' : 3, 'due_date' : '9.30.2020', 'template': templates[1]},
    {'id' : 4, 'due_date' : '10.5.2020', 'template': templates[1]},
    {'id' : 5, 'due_date' : '10.5.2020', 'template': templates[2]},
    {'id' : 6, 'due_date' : '10.10.2020', 'template': templates[1]},
    ]
    form = ChangeViewForm()
    if form.validate_on_submit():
        view = form.select_view.data
        change_view = {'view': view}
        user.update(change_view)
        return render_template('user/home.html', title="Home", tasks=tasks, user=user, form=form)
    return render_template('user/home.html', title="Home", tasks=tasks, user=user, form=form)
