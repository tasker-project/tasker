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
            starting_date_obj):
        job_template = cls(
            name=name, description=description, repetition=repetition,
            interval=interval, hour=hour,
            starting_date=int(starting_date_obj.timestamp())
        )
        db.session.add(job_template)
        db.session.commit()
        return job_template

    @classmethod
    def getJobTemplates(cls):
        query = db.session.query(JobTemplate)
        return query
