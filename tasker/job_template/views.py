from flask import Blueprint, render_template, redirect, url_for, flash
from tasker.models import db
#from tasker.job_template.forms import JobTemplateForm
from tasker.models import JobTemplate

bp = Blueprint('job_template', __name__, static_folder='../static')

@bp.route('/templates')
#@login_required
def templates():
    jobs = JobTemplate.getJobTemplates()
    
    return render_template('job-template/templates.html', title='Templates', jobs=jobs)

@bp.route('/add_template')
#@login_required
def add_template():
    return render_template('job-template/add-template.html', title="Create Template")

@bp.route('/template_detail/<id>')
#@login_required
def template_detail(id):
    job = JobTemplate.getJobTemplate(id)

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
