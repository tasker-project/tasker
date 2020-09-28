# 2020-09-19 16:30:14 -0700 - Emily Martens - add task blueprint with routes to task detail - lines:,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33
# 2020-09-19 19:02:54 -0700 - Emily Martens - add views and navigation for add template, add task, and archive. - lines:,34,35,36,37,38,39,46,47,48,49
# 2020-09-23 23:09:41 -0400 - Jeremy Axmacher - Team collaborated on model schema definition - lines:,6
# 2020-09-19 19:46:10 -0700 - Emily Martens - add snooze and delete views, update styles - lines:,5,40,41,42,43,44,45,50,51,52,53,54,55,56
from flask import Blueprint, render_template, flash, redirect, url_for
from tasker.models import db
#from tasker.task.forms import EditTaskForm, SnoozeTaskForm

bp = Blueprint('task', __name__, static_folder='../static')

@bp.route('/task_detail/<id>')
def task_detail(id):
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

    task = tasks[int(id)]

    return render_template("task/task-detail.html", title="Task Detail", user=user, task=task)

@bp.route('/add_task')
#@login_required
def add_task():
    return render_template('task/add-task.html', title="Create Task")

@bp.route('/snooze/<id>')
#@login_required
def snooze(id):
    id=id
    return render_template('task/snooze.html', title="Snooze", id=id)

@bp.route('/archive')
#@login_required
def archive():
    return render_template('task/archive.html', title="Archive")

@bp.route('/delete_task/<id>')
#@login_required
def delete_task(id):
    id=id
    flash("Task deleted: " + id)
    return redirect(url_for('user.home'))
