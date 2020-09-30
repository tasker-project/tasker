# 2020-09-24 22:26:17 -0700 - Emily Martens - debug login_manager, add full login functionality, add logout route to menu - lines:,32,33,34,35,36,37,38,39
# 2020-09-27 13:28:53 -0700 - Emily Martens - fix naming discrepancies in user forms/views/templates, add form styling classes to register template, restructure login and register templates to match, re-enable User blueprint. - lines:,44,45
# 2020-09-25 07:30:26 -0700 - Maged Bebawy - added user registeration - lines:,10,12,16,30
# 2020-09-24 21:54:21 -0700 - Emily Martens - add login setup, form, view, template, add logout route - lines:,13,40,62
# 2020-09-23 23:09:41 -0400 - Jeremy Axmacher - Team collaborated on model schema definition - lines:,7,8,9,11,14,15,17,18,19,20,21,22,23,24,25,26,27,28,29,31,41,42,43,46,47,48,52,53,54,55,56,57,58,59,60,61
# 2020-09-29 16:36:00 -0400 - Jeremy Axmacher - Clean up job template form and job template detail field formatting - lines:,49,50,51
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
    app.jinja_env.filters['friendly_date'] = job_template.views.friendly_date
    app.jinja_env.filters['intervalify'] = job_template.views.intervalify
    app.jinja_env.filters['hourify'] = job_template.views.hourify

    from tasker import task
    app.register_blueprint(task.views.bp)

    @app.cli.command('create-db')
    def create_db():
        with create_app().app_context():
            from tasker.models import db
            db.create_all()

    return app
