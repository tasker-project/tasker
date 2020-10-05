from flask import Blueprint, render_template, flash, redirect, url_for, request
import pytz, datetime
from pytz import timezone
from tasker.models import db, Task, TaskStatus
from flask_login import current_user, login_required
from tasker.task.forms import SnoozeTaskForm, DeleteTastForm

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

@bp.route('/task_complete/<id>')
@login_required
def task_complete(id):
    task = Task.query.get(id)
    if not task.owner == current_user:
        flash("Unexpected task error. Please try again.", 'error')
        return redirect(url_for('user.home'))
    task.status = TaskStatus.Completed
    db.session.add(task)
    db.session.commit()
    flash("Task marked complete", 'success')
    return redirect(url_for('user.home'))


@bp.route('/snooze/<id>', methods=['GET', 'POST'])
@login_required
def snooze(id):
    task = Task.query.get(id)
    if not task.owner == current_user:
        flash("Unexpected task error. Please try again.", 'error')
        return redirect(url_for('user.home'))
    form = SnoozeTaskForm()
    if form.validate_on_submit():
        user_tz = timezone(current_user.timezone)
        due = form.due_date.data
        snooze_date = datetime.datetime.combine(due, datetime.time(task.job_template.hour, 0))
        snooze_date = user_tz.localize(snooze_date)
        task.due_date = int(snooze_date.timestamp())
        task.status = TaskStatus.Snoozed
        desc = task.description
        note = form.note.data
        task.description = desc + "\n" + note
        db.session.add(task)
        db.session.commit()
        flash("Task Snoozed", 'success')
        return redirect(url_for('user.home'))
    return render_template('task/snooze.html', title="Snooze", task=task, form=form)

@bp.route('/archive')
@login_required
def archive():
    tasks = Task.query.filter(Task.owner == current_user, Task.status == TaskStatus.Completed)
    return render_template('task/archive.html', title="Archive", tasks=tasks)

@bp.route('/delete_task/<id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    task = Task.query.get(id)
    form = DeleteTastForm()
    if not task.owner == current_user:
        flash("Unexpected task error. Please try again.", 'error')
        return redirect(url_for('user.home'))
    if request.method == 'POST':
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully', 'success')
        return redirect(url_for('user.home'))
    return render_template('task/delete_task.html', task=task, id=id, form=form)
