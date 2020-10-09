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
        task.description = desc + "\n" + note
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
        form = TaskForm(obj=task)
        due_date = user_tz.localize(datetime.fromtimestamp(task.due_date))
        form.due_date.data = due_date.date()
    if form.validate_on_submit():
        user_tz = timezone(current_user.timezone)
        due_date = user_tz.localize(datetime.combine(form.due_date.data, datetime.min.time()))
        task.name = form.name.data
        task.description = form.description.data
        task.due_date =  int(due_date.timestamp())
        task.hour = form.hour.data
        db.session.add(task)
        db.session.commit()
        flash('Successfully updated task', 'success')
        return redirect(url_for('task.details', id=task.id))
    return render_template('task/edit-task.html', title="Edit Task", form=form)
