from tasker.database import db

class User(db.Model):
    name = db.Column(db.String(20), primary_key=True)