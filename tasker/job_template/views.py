from datetime import datetime

from werkzeug.exceptions import NotFound
import pytz
from pytz import timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from tasker.models import db, JobTemplate
from tasker.job_template.forms import JobTemplateForm
from tasker.job_template.generate import generate_tasks, delete_tasks

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
        delete_tasks(template.id)
        generate_tasks(template.id)
        flash('Successfully updated template', 'success')
        return redirect(url_for('job_template.template_detail', id=template.id))
    return render_template('job-template/edit-template.html', title="Edit Template", form=form)


@bp.route('/delete_template/<id>')
#@login_required
def delete_template(id):
    id=id
    flash("Template deleted")
    return redirect(url_for('job_template.templates'))
