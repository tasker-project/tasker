from pathlib import Path
import os

from flask import Flask, flash
from flask_bcrypt import Bcrypt
from flask_moment import Moment
from flask_login import LoginManager

bcrypt = Bcrypt()
moment = Moment()

def create_app(config_object='tasker.settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect()
    csrf.init_app(app)

    from tasker.models import db
    db.init_app(app)

    bcrypt.init_app(app)
    moment.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    from tasker.models import User
    @login_manager.user_loader
    def load_user(email):
        return User.query.get(email)

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
            from tasker.models import db
            db.create_all()

    return app
