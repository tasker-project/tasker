# 2020-09-23 09:56:33 -0700 - Maged Bebawy - started working on forms and models files - lines:,24,33,41,42,43,46,67,68,71,72
# 2020-09-19 13:07:50 -0700 - Emily Martens - add front end setup, blueprint setup for user, job_template - lines:,9,14,21,22,44,45,47,54
# 2020-09-29 16:36:00 -0400 - Jeremy Axmacher - Add initial job template form and creation logic - lines:,80,84,85
# 2020-09-25 07:30:26 -0700 - Maged Bebawy - added user registeration - lines:,58,79,82
# 2020-09-24 21:54:21 -0700 - Emily Martens - add login setup, form, view, template, add logout route - lines:,30,64,65,89
# 2020-09-23 23:09:41 -0400 - Jeremy Axmacher - Team collaborated on model schema definition - lines:,8,10,11,12,13,15,16,17,18,19,20,23,25,26,27,28,29,31,32,34,35,36,37,38,39,40,48,49,50,51,52,53,55,57,59,60,61,62,63,66,69,70,73,74,75,76,77,78,81,83,86,87,88
# 2020-09-24 17:39:34 -0400 - Jeremy Axmacher - Remove hardcoded ID from task and job template creation - lines:,56
import enum
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from tasker.app import bcrypt

db = SQLAlchemy()

class TaskStatus(enum.Enum):
    Pending = 1
    Due = 2
    Snoozed = 3
    Completed = 4



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    email_address = db.Column(db.String(345), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    timezone = db.Column(db.String(80), nullable=False)
    templates = db.relationship('JobTemplate', backref='owner', lazy='dynamic')
    tasks = db.relationship('Task', backref='owner', lazy='dynamic')

    def get_id(self):
        return self.email_address

    @classmethod
    def create_user(cls, email_address, password, timezone):
        user = cls(
            email_address=email_address,
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
            timezone=timezone
        )
        db.session.add(user)
        db.session.commit()
        return user

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(4096), default='')
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.Pending)
    due_date = db.Column(db.Integer)
    user_email_address = db.Column(db.String(345), db.ForeignKey('user.email_address'))
    job_template_id = db.Column(db.Integer, db.ForeignKey('job_template.id'))

    @classmethod
    def create_task(cls, name, description, status, due_date_obj):
        task = cls(
            name=name, description=description, status=status,
            due_date=int(due_date_obj.timestamp())
        )
        db.session.add(task)
        db.session.commit()
        return task


class JobTemplate(db.Model):
    __tablename__ = 'job_template'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(4096), default='')
    repetition = db.Column(db.Integer)
    interval = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    starting_date = db.Column(db.Integer)
    user_email_address = db.Column(db.String(345), db.ForeignKey('user.email_address'))
    tasks = db.relationship('Task', backref='job_template', uselist=True)

    @classmethod
    def create_job_template(cls, name, description, repetition, interval, hour,
            starting_date_obj, user):
        job_template = cls(
            name=name, description=description, repetition=repetition,
            interval=interval, hour=hour,
            starting_date=int(starting_date_obj.timestamp()),
            user_email_address=user.email_address
        )
        db.session.add(job_template)
        db.session.commit()
        return job_template
