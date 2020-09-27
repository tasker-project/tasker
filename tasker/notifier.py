import time
import datetime
from tasker.models import db, Task, TaskStatus
from tasker import create_app

import pytz
import boto3
from flask import render_template

email_service = boto3.client('ses')
# 30 minute time buffer for querying pending tasks
time_buffer = 60 * 30


def send_email(task):
    due_date = datetime.datetime.fromtimestamp(task.due_date, tz=pytz.timezone(task.owner.timezone))
    due_date = due_date.strftime('%B %d, %Y %I:%M%p')
    html_template = render_template('notifier/email.html', task=task, due_date=due_date)
    text_template = render_template('notifier/email.txt', task=task, due_date=due_date)
    response = email_service.send_email(
        Destination={'ToAddresses': [task.user_email_address]},
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': html_template
                },
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': text_template
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': f'Task Due - {task.name}'
            }
        },
        Source='Tasker <app@tasker.nvram.io>'
    )


def notify():
    app = create_app()
    with app.app_context():
        # Get all pending or snoozed tasks with
        # due dates less than 30 minutes from now
        time_guard = int(time.time() + time_buffer)
        tasks = Task.query.filter(
            Task.due_date < time_guard,
            Task.status.in_([TaskStatus.Pending, TaskStatus.Snoozed])
        )
        for task in tasks:
            send_email(task)
            task.status = TaskStatus.Due
            db.session.add(task)
            db.session.commit()


if __name__ == '__main__':
    notify()