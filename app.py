# 2020-09-19 13:07:50 -0700 - Emily Martens - add front end setup, blueprint setup for user, job_template - lines:,21,22,23,24,25,26,27,28
# 2020-09-19 16:30:14 -0700 - Emily Martens - add task blueprint with routes to task detail - lines:,30,31,32
# 2020-09-10 17:51:11 -0400 - Jeremy Axmacher - Initial commit - lines:,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,29,33,34,35,36,37,38,39,40,41
from pathlib import Path
import os

from flask import Flask


def create_app(config_object='tasker.settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect()
    csrf.init_app(app)

    from tasker.database import db
    db.init_app(app)

    #from tasker import home
    #app.register_blueprint(home.views.blueprint)

    from tasker import user
    app.register_blueprint(user.views.bp)

    from tasker import job_template
    app.register_blueprint(job_template.views.bp)

    from tasker import task
    app.register_blueprint(task.views.bp)

    @app.cli.command('create-db')
    def create_db():
        with create_app().app_context():
            from tasker.database import db
            # Add all models here so that they register themselves to the db
            from tasker.home.models import User
            db.create_all()

    return app
