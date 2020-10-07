# 2020-09-27 12:15:15 -0400 - Jeremy Axmacher - Add logging for monitoring purposes - lines:,4,5,6,8,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,35,38,41,65,71,72,73,74,75,76,77,78,79,81,82,84,86,90
# 2020-09-27 01:43:33 -0400 - Jeremy Axmacher - Add email notifier - lines:,3,7,9,28,29,30,31,32,33,34,36,37,39,40,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,67,68,69,70,80,83,85,87,88,89,91,92,93,94
import datetime
import logging
import time
import sys

from sqlalchemy.orm import joinedload
from flask import render_template
import boto3
import pytz

from tasker import create_app
from tasker.models import db, Task, TaskStatus

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('botocore.client').setLevel(logging.INFO)
logging.getLogger('botocore.hooks').setLevel(logging.INFO)
logging.getLogger('botocore.endpoint').setLevel(logging.INFO)
logging.getLogger('botocore.auth').setLevel(logging.INFO)

email_service = boto3.client('ses')
# 30 minute time buffer for querying pending tasks
time_buffer = 60 * 30


def send_email(task):
    logging.debug('Formatting due date for task: %r', task)
    due_date = datetime.datetime.fromtimestamp(task.due_date, tz=pytz.timezone(task.owner.timezone))
    due_date = due_date.strftime('%B %d, %Y %I:%M%p')
    logging.debug('Rendering templates for task: %r', task)
    html_template = render_template('notifier/email.html', task=task, due_date=due_date)
    text_template = render_template('notifier/email.txt', task=task, due_date=due_date)
    logging.debug('Sending email to user: %s', task.user_email_address)
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
    logger.info('Starting up. Creating Flask app context.')
    app = create_app()
    with app.app_context():
        # Get all pending or snoozed tasks with
        # due dates less than 30 minutes from now
        time_guard = int(time.time() + time_buffer)
        logger.info('Querying for tasks pending or snoozed which are due before %s', time_guard)
        tasks = list(Task.query.\
            options(
                joinedload(Task.owner)
            ).\
            filter(
                Task.due_date < time_guard,
                Task.status.in_([TaskStatus.Pending, TaskStatus.Snoozed])
            )
        )
        if not tasks:
            logging.info('No tasks to process.')
        for task in tasks:
            logging.info('Processing task: %r', task)
            send_email(task)
            logging.info('Email sent for task: %r', task)
            task.status = TaskStatus.Due
            db.session.add(task)
            db.session.commit()
            logging.info('Task status changed to pending: %r', task)


if __name__ == '__main__':
    notify()
