from werkzeug.security import generate_password_hash, check_password_hash
from tasker.database import db
#from tasker.app import login
from flask_login import UserMixin

#@login.user_loader
#def load_user(id):
    #return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    time_zone = db.Column(db.String(120))
    templates = db.relationship('JobTemplate', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class JobTemplate(db.Model):
    __tablename__ = "job-template"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    start_date = db.Column(db.DateTime())
    interval = db.Column(db.Integer)
    interval_type = db.Column(db.String(60))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tasks = db.relationship('Task', backref='template', lazy='dynamic')

class Task(db.Model):
    __tablename__ = "job-template"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('job-template.id'))
    due_date = db.Column(db.DateTime())
    is_complete = db.Column(db.Boolean(), default=False)
    is_snoozed = db.Column(db.Boolean(), default=False)

    def set_complete(self, status):
        self.is_complete = status

    def set_snoozed(self, due_date):
        self.due_date = due_date
        self.is_snoozed = True
