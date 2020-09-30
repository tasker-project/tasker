# 2020-09-19 14:02:51 -0700 - Emily Martens - add more views to job_template bp, add task detail html page. - lines:,56,76,78
# 2020-09-28 13:54:32 -0400 - ADM Wayne Bryan - Added views for job template list, and details of a single job template - lines:,55,90
# 2020-09-19 13:07:50 -0700 - Emily Martens - add front end setup, blueprint setup for user, job_template - lines:,21,22,23,51,53
# 2020-09-19 19:02:54 -0700 - Emily Martens - add views and navigation for add template, add task, and archive. - lines:,60,75
# 2020-09-29 16:36:00 -0400 - Jeremy Axmacher - Add initial job template form and creation logic - lines:,10,11,12,13,14,17,18,19,20,24,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,57,58,59,61,62,63,64,65,66,67,68,69,70,71,72,73,74,98
# 2020-09-28 13:34:04 -0400 - ADM Wayne Bryan - save - lines:,89
# 2020-09-29 10:49:20 -0400 - ADM Wayne Bryan - Moved query code to views.py
Modified queries to filter based on user id of logged in user
Added exception for job template not found - lines:,16,52,54,77,79,80,81,82,83,84,85,86,87,88
# 2020-09-19 19:46:10 -0700 - Emily Martens - add snooze and delete views, update styles - lines:,15,91,92,93,94,95,96,97,99,100,101,102,103,104
# 2020-09-29 16:36:00 -0400 - Jeremy Axmacher - Clean up job template form and job template detail field formatting - lines:,27
from datetime import datetime

from werkzeug.exceptions import NotFound
import pytz
from pytz import timezone
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from tasker.models import db, JobTemplate
from tasker.job_template.forms import JobTemplateForm
from tasker.job_template.generate import generate_tasks

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
    return render_template('job-template/add-template.html', title="Create Template", form=form, user=current_user)


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

@bp.route('/edit_template/<id>')
#@login_required
def edit_template(id):
    id = id
    return render_template('job-template/edit-template.html', title="Edit Template", id=id)


@bp.route('/delete_template/<id>')
#@login_required
def delete_template(id):
    id=id
    flash("Template deleted")
    return redirect(url_for('job_template.templates'))
