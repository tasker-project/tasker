from tasker.models import db, User, JobTemplate, Task, TaskStatus
import datetime, pytz
from pytz import timezone

def generate_tasks(template_id):
    template = JobTemplate.query.get(template_id)
    user = template.owner
    rep = template.repetition
    interval = template.interval
    user_tz = timezone(user.timezone)
    if interval == 2:
        rep *= 7
    if interval == 3:
        rep *= 30
    timestamp = datetime.datetime.fromtimestamp(
        template.starting_date,
        tz=pytz.timezone(user.timezone)
    )
    start = timestamp.date()
    end = start.replace(start.year + 1)
    while start <= end:
        timestamp = datetime.datetime.combine(start, datetime.time(template.hour, 0))
        timestamp = user_tz.localize(timestamp)
        task = Task.create_task(template.name, template.description,TaskStatus.Pending, timestamp)
        task.owner = user
        task.job_template = template
        db.session.add(task)
        start += datetime.timedelta(days=rep)
    db.session.commit()
    return 1


def delete_tasks(template_id):
    template = JobTemplate.query.get(template_id)
    tasks = Task.query.filter(Task.job_template == template, Task.status != TaskStatus.Completed)
    for t in tasks:
        db.session.delete(t)
    db.session.commit()
    return 1


def update_job_template(template_id):
    delete_tasks(template_id)
    generate_tasks(template_id)
