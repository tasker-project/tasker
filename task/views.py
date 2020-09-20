from flask import Blueprint, render_template, flash, redirect, url_for
from tasker.database import db
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
