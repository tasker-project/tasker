# 2020-10-05 08:28:49 -0400 - ADM Wayne Bryan - Added form to create a single task, /add_task - lines:,19,23,29,30,32,33,34,35,37,38,39,40,41,42,43,44,45
# 2020-10-04 19:49:38 -0700 - Emily Martens - add completed button, routing. delete old home blueprint and jinja template. - lines:,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,72
# 2020-09-19 16:30:14 -0700 - Emily Martens - add task blueprint with routes to task detail - lines:,26,27,28
# 2020-09-19 19:02:54 -0700 - Emily Martens - add views and navigation for add template, add task, and archive. - lines:,31,47,92,94
# 2020-10-04 23:10:10 -0700 - Maged Bebawy - Added delete task - lines:,21,98,99,101,103,104,105,106,107,108,109,110,111
# 2020-10-06 17:24:32 -0400 - ADM Wayne Bryan - Removed saving hour to Task data
Added hour component to Task.due_date - lines:,36
# 2020-10-10 21:50:54 -0400 - Jeremy Axmacher - Fix timezone localization - lines:,132
# 2020-10-04 22:01:48 -0400 - Jeremy Axmacher - Add archive view and clean up job templates list formatting - lines:,93,95,96
# 2020-10-10 09:54:35 -0400 - Jeremy Axmacher - Fix edit form so that task due hour is populated in form and saved to task. - lines:,133,134,135,136,137,138,142
# 2020-10-04 23:16:55 -0700 - Maged Bebawy - Added delete task - lines:,102
# 2020-10-04 14:05:29 -0700 - Emily Martens - complete snooze functionality and db operations. - lines:,22,75,76,77,80,81,82,83,84,85,86,87,88,89
# 2020-10-08 07:17:14 -0700 - Maged Bebawy - added task details - lines:,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,139,140,141,143,144,145,146,147,148,149,150
# 2020-10-05 12:00:29 -0400 - ADM Wayne Bryan - Removed job template selection for creating single task - lines:,46
# 2020-10-06 21:05:59 -0400 - J Axmacher - Merge branch 'master' into wayne-task-views - lines:,18,20,25
# 2020-10-07 20:15:53 -0700 - Emily Martens - fix snooze to work with template-based and one-time tasks, remove zip folder. - lines:,66,67,68,69,70,78,79,90
# 2020-09-19 19:46:10 -0700 - Emily Martens - add snooze and delete views, update styles - lines:,64,91,97,100
# 2020-10-04 12:16:06 -0700 - Emily Martens - add Snooze form and template fields - lines:,24,62,65,71,73,74
from datetime import datetime, timedelta, time
import pytz

from flask import Blueprint, render_template, flash, redirect, url_for, request
from pytz import timezone
from tasker.models import db, Task, TaskStatus, JobTemplate
from flask_login import current_user, login_required
from tasker.task.forms import TaskForm, SnoozeTaskForm, DeleteTaskForm

bp = Blueprint('task', __name__, static_folder='../static')

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
    old_ts = datetime.fromtimestamp(
        task.due_date,
        tz=pytz.timezone(current_user.timezone)
    )
    old_hr = old_ts.hour
    if not task.owner == current_user:
        flash("Unexpected task error. Please try again.", 'error')
        return redirect(url_for('user.home'))
    form = SnoozeTaskForm()
    if form.validate_on_submit():
        user_tz = timezone(current_user.timezone)
        due = form.due_date.data
        hour = int(form.hour.data)
        snooze_date = datetime.combine(due, time(hour, 0))
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
    return render_template('task/snooze.html', title="Snooze", task=task, form=form, hour=old_hr)

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

@bp.route('/details/<id>')
@login_required
def details(id):
    task = Task.query.get(id)
    if not task.owner == current_user:
        flash("Unexpected task error. Please try again.", 'error')
        return redirect(url_for('user.home'))
    return render_template('task/details.html', title='Task Details', task=task, id=id)

@bp.route('/edit_task/<id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    form = TaskForm()
    task = Task.query.get(id)
    user_tz = timezone(current_user.timezone)
    if not task.owner == current_user:
        flash("Unexpected task error. Please try again.", 'error')
        return redirect(url_for('user.home'))
    if request.method == 'GET':
        due_date = datetime.fromtimestamp(task.due_date, tz=user_tz)
        form = TaskForm(
            name=task.name,
            description=task.description,
            due_date=due_date.date(),
            hour=due_date.hour
        )
    if form.validate_on_submit():
        user_tz = timezone(current_user.timezone)
        due_date = user_tz.localize(datetime.combine(form.due_date.data, datetime.min.time()))
        due_date = due_date + timedelta(hours=int(form.hour.data))
        task.name = form.name.data
        task.description = form.description.data
        task.due_date =  int(due_date.timestamp())
        db.session.add(task)
        db.session.commit()
        flash('Successfully updated task', 'success')
        return redirect(url_for('task.details', id=task.id))
    return render_template('task/edit-task.html', title="Edit Task", form=form)
