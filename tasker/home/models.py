# 2020-09-10 17:51:11 -0400 - Jeremy Axmacher - Initial commit - lines:,2,3,4,5
from tasker.database import db

class User(db.Model):
    name = db.Column(db.String(20), primary_key=True)
