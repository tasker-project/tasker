# 2020-09-26 19:00:23 -0700 - Emily Martens - move commit outside of loop in generate_tasks - lines:,34
# 2020-09-26 19:43:04 -0700 - Emily Martens - add hour and localize to timezone for generate_tasks - lines:,6,7
# 2020-09-25 23:22:17 -0700 - Emily Martens - add Job Template task generation function, Job Template task deletion function, and Job Template update Tasks function. - lines:,5,9,10,11,12,13,14,16,17,18,19,29,30,31,32,35,36,37,38,39,40,41,42,43,44,45,46,47,48
# 2020-09-29 16:36:00 -0400 - Jeremy Axmacher - Fix task timestamp calculation to account for daylight savings - lines:,8,15,20,21,22,23,24,25,26,27,28,33
from tasker.models import db, User, JobTemplate, Task, TaskStatus
from pytz import timezone
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
    tasks = Task.query.filter_by(job_template=template)
    for t in tasks:
        db.session.delete(t)
    db.session.commit()
    return 1

def update_job_template(template_id):
    delete_tasks(template_id)
    generate_tasks(template_id)
    return 1
