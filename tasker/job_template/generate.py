from tasker.models import db, User, JobTemplate, Task, TaskStatus
import datetime

def generate_tasks(template_id):
    template = JobTemplate.query.get(template_id)
    user = template.owner
    rep = template.repetition
    interval = template.interval
    if interval == 2:
        rep *= 7
    if interval == 3:
        rep *= 30
    start = template.starting_date
    timestamp = datetime.datetime.fromtimestamp(start)
    end = timestamp.replace(timestamp.year + 1)
    while timestamp <= end:
        task = Task.create_task(template.name, template.description,TaskStatus.Pending, timestamp)
        task.owner = user
        task.job_template = template
        db.session.add(task)
        db.session.commit()
        timestamp += datetime.timedelta(days=rep)
    return 1

def delete_tasks(template_id):
    template = JobTemplate.query.get(template_id)
    tasks = Task.query.filter_by(job_template=template)
    for t in tasks:
        db.session.delete(t)
    db.session.commit()
    return 1

def update_job_template(template_id):
    delete_tasks(template_id)
    generate_tasks(template_id)
    return 1
