# 2020-09-19 14:02:51 -0700 - Emily Martens - add more views to job_template bp, add task detail html page. - lines:,57,77,79
# 2020-09-28 13:54:32 -0400 - ADM Wayne Bryan - Added views for job template list, and details of a single job template - lines:,56,91
# 2020-10-04 23:26:44 -0400 - Jeremy Axmacher - Add job template deletion - lines:,20,21,117,123,124,126,127,128,129,130,131,132,133,134,135,136,137,138
# 2020-09-19 13:07:50 -0700 - Emily Martens - add front end setup, blueprint setup for user, job_template - lines:,22,23,24,52,54
# 2020-09-19 19:02:54 -0700 - Emily Martens - add views and navigation for add template, add task, and archive. - lines:,61,76
# 2020-09-29 16:36:00 -0400 - Jeremy Axmacher - Add initial job template form and creation logic - lines:,12,13,14,15,18,19,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,58,59,60,62,63,64,65,66,67,68,69,70,71,72,73,75,122
# 2020-09-28 13:34:04 -0400 - ADM Wayne Bryan - save - lines:,90
# 2020-10-04 23:26:44 -0400 - Jeremy Axmacher - Add job template editing - lines:,16,74,93,94,95,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,118,119,120
# 2020-09-29 10:49:20 -0400 - ADM Wayne Bryan - Moved query code to views.py
Modified queries to filter based on user id of logged in user
Added exception for job template not found - lines:,17,53,55,78,80,81,82,83,84,85,86,87,88,89
# 2020-09-19 19:46:10 -0700 - Emily Martens - add snooze and delete views, update styles - lines:,92,96,121,125
# 2020-09-29 16:36:00 -0400 - Jeremy Axmacher - Clean up job template form and job template detail field formatting - lines:,28
from datetime import datetime
from werkzeug.exceptions import NotFound
import pytz
from pytz import timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from tasker.models import db, JobTemplate
from tasker.job_template.forms import JobTemplateForm, DeleteConfirmationForm
from tasker.job_template.generate import generate_tasks, delete_tasks, update_job_template

bp = Blueprint('job_template', __name__, static_folder='../static')


def friendly_date(d):
    starting_date = datetime.fromtimestamp(d, tz=pytz.timezone(current_user.timezone))
    return starting_date.strftime('%B %d, %Y')


def intervalify(i):
    if i == 1:
        return 'Day(s)'
    elif i == 2:
        return 'Week(s)'
    else:
        return 'Month(s)'


def hourify(h):
    if h < 12:
        suffix = 'AM'
        if h == 0:
            h = '12'
    else:
        suffix = 'PM'
        if h > 12:
            h = h - 12
    return f'{h} {suffix}'


@bp.route('/templates')
@login_required
def templates():
    jobs = db.session.query(JobTemplate).filter(JobTemplate.user_email_address == current_user.email_address)
    return render_template('job-template/templates.html', title='Templates', jobs=jobs)


@bp.route('/add_template', methods=['GET', 'POST'])
@login_required
def add_template():
    form = JobTemplateForm()
    if form.validate_on_submit():
        user_tz = timezone(current_user.timezone)
        starting_date = user_tz.localize(datetime.combine(form.starting_date.data, datetime.min.time()))
        template = JobTemplate.create_job_template(
            form.name.data, form.description.data,
            form.repetition.data, form.interval.data,
            form.hour.data, starting_date, current_user
        )
        generate_tasks(template.id)
        flash('Successfully created template', 'success')
        return redirect(url_for('user.home'))
    return render_template('job-template/add-template.html', title="Create Template", form=form)


@bp.route('/template_detail/<id>')
@login_required
def template_detail(id):
    job = JobTemplate
    foundJob = False
    query = db.session.query(JobTemplate).filter(JobTemplate.id == id and JobTemplate.user_email_address == current_user.email_address)
    for record in query:
        job = record
        foundJob = True

    #throw error when job template does not exist, or not owned by user
    if not foundJob:
        raise NotFound('Job template not found')

    return render_template('job-template/template-detail.html', title='Template Details', job=job)


@bp.route('/edit_template/<id>', methods=['GET', 'POST'])
@login_required
def edit_template(id):
    form = JobTemplateForm()
    template = JobTemplate.query.get_or_404(id)
    user_tz = timezone(current_user.timezone)
    if template.owner != current_user:
        raise NotFound('Template not found')
    if request.method == 'GET':
        form = JobTemplateForm(obj=template)
        starting_date = user_tz.localize(datetime.fromtimestamp(template.starting_date))
        form.starting_date.data = starting_date.date()
    if form.validate_on_submit():
        user_tz = timezone(current_user.timezone)
        starting_date = user_tz.localize(datetime.combine(form.starting_date.data, datetime.min.time()))
        template.name = form.name.data
        template.description = form.description.data
        template.repetition = form.repetition.data
        template.interval = form.interval.data
        template.hour = form.hour.data
        template.starting_date = int(starting_date.timestamp())
        db.session.add(template)
        db.session.commit()
        update_job_template(template.id)
        flash('Successfully updated template', 'success')
        return redirect(url_for('job_template.template_detail', id=template.id))
    return render_template('job-template/edit-template.html', title="Edit Template", form=form)


@bp.route('/delete_template/<id>', methods=['GET', 'POST'])
@login_required
def delete_template(id):
    form = DeleteConfirmationForm()
    template = JobTemplate.query.get_or_404(id)
    name = template.name
    if template.owner != current_user:
        raise NotFound('Template not found')
    if form.validate_on_submit():
        delete_tasks(template.id)
        db.session.delete(template)
        db.session.commit()
        flash("Template deleted")
        flash(f'Successfully deleted template: {name}', 'success')
        return redirect(url_for('user.home'))
    return render_template('job-template/delete-template.html', title="Delete Template?", form=form, id=id, name=name)
