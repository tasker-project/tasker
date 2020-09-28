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


@bp.template_filter('friendly_date')
def friendly_date(d):
    starting_date = datetime.fromtimestamp(d, tz=pytz.timezone(current_user.timezone))
    return starting_date.strftime('%B %d, %Y %I:%M%p')


@bp.template_filter('intervalify')
def intervalify(i):
    if i == 1:
        return 'Day(s)'
    elif i == 2:
        return 'Week(s)'
    else:
        return 'Month(s)'


@bp.template_filter('hourify')
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
