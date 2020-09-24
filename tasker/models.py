from werkzeug.security import generate_password_hash, check_password_hash
from tasker.database import db
#from tasker.app import login
from flask_login import UserMixin

#@login.user_loader
#def load_user(id):
    #return User.query.get(int(id))



class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email_address = db.Column(db.String(250), nullable=False)
    time_zone = db.Column(db.String(80), nullable=False)
    registeration_date = db.Column(db.DateTime, default=datetime.now)
    templates = db.relationship('Job_template', backref='owner', lazy='dynamic')
    
    @classmethod
    def create_user(cls, user, password, fname, lname, email, timezone):

        user = cls(user_name=user, password=bcrypt.generate_password_hash(password).decode('utf-8'),
                    first_name=fname, last_name=lname, email_address=email, 
                    time_zone=timezone)
        
        db.session.add(user)
        db.session.commit()
        return user

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    is_snoozed = db.Column(db.Boolean(), default=False)
    due_date = db.Column(db.DateTime())
    job_template_id = db.Column(db.Integer, db.Foreignkey('job_template.id'))

    
        
class Job_template(db.Model):
    __tablename__ = 'job_template'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    repetition = db.Column(db.Integer)
    interval = db.Column(db.Integer)
    current_date = db.Column(db.DateTime(), nullable=False)
    owner_id = db.Column(db.Integer, db.Foreignkey('user.id')
    task = db.relationship('Task', backref='job_template' uselist=False)
    
    
    
        
