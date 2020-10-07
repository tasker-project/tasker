# 2020-10-05 08:28:49 -0400 - ADM Wayne Bryan - Added form to create a single task, /add_task - lines:,15,19,49,50,52,53,54,55,57,58,59,60,61,62,63,64,65
# 2020-10-04 19:49:38 -0700 - Emily Martens - add completed button, routing. delete old home blueprint and jinja template. - lines:,68,69,70,71,72,73,74,75,76,77,78,79,80,81,83,87
# 2020-09-19 16:30:14 -0700 - Emily Martens - add task blueprint with routes to task detail - lines:,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47
# 2020-09-19 19:02:54 -0700 - Emily Martens - add views and navigation for add template, add task, and archive. - lines:,48,51,67,106,108
# 2020-10-04 23:10:10 -0700 - Maged Bebawy - Added delete task - lines:,17,112,113,115,117,118,119,120,121,122,123,124,125
# 2020-10-06 17:24:32 -0400 - ADM Wayne Bryan - Removed saving hour to Task data
Added hour component to Task.due_date - lines:,56
# 2020-10-04 22:01:48 -0400 - Jeremy Axmacher - Add archive view and clean up job templates list formatting - lines:,107,109,110
# 2020-10-04 23:16:55 -0700 - Maged Bebawy - Added delete task - lines:,116
# 2020-10-04 14:05:29 -0700 - Emily Martens - complete snooze functionality and db operations. - lines:,18,90,91,92,94,95,96,97,98,99,100,101,102,103
# 2020-10-05 12:00:29 -0400 - ADM Wayne Bryan - Removed job template selection for creating single task - lines:,66
# 2020-10-06 21:05:59 -0400 - J Axmacher - Merge branch 'master' into wayne-task-views - lines:,14,16,21,93
# 2020-09-19 19:46:10 -0700 - Emily Martens - add snooze and delete views, update styles - lines:,84,105,111,114
# 2020-10-04 12:16:06 -0700 - Emily Martens - add Snooze form and template fields - lines:,20,82,85,86,88,89,104
from datetime import datetime, timedelta, time
import pytz

from flask import Blueprint, render_template, flash, redirect, url_for, request
from pytz import timezone
from tasker.models import db, Task, TaskStatus, JobTemplate
from flask_login import current_user, login_required
from tasker.task.forms import TaskForm, SnoozeTaskForm, DeleteTaskForm

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

@bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        user_tz = timezone(current_user.timezone)
        due_date = user_tz.localize(datetime.combine(form.due_date.data, datetime.min.time()))
        due_date = due_date + timedelta(hours=int(form.hour.data))
        task = Task.create_task(
            form.name.data, form.description.data,
            TaskStatus.Pending, due_date
        )
        task.owner = current_user
        db.session.add(task)
        db.session.commit()
        flash('Successfully created task', 'success')
        return redirect(url_for('user.home'))
    return render_template('task/add-task.html', title="Create Task", form=form)

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
        snooze_date = datetime.combine(due, time(task.job_template.hour, 0))
        snooze_date = user_tz.localize(snooze_date)
        task.due_date = int(snooze_date.timestamp())
        task.status = TaskStatus.Snoozed
        desc = task.description
        note = form.note.data
        task.description = desc + "
" + note
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
    form = DeleteTaskForm()
    if not task.owner == current_user:
        flash("Unexpected task error. Please try again.", 'error')
        return redirect(url_for('user.home'))
    if request.method == 'POST':
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully', 'success')
        return redirect(url_for('user.home'))
    return render_template('task/delete_task.html', task=task, id=id, form=form)
