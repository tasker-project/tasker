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

    @app.cli.command('create-db')
    def create_db():
        with create_app().app_context():
            from tasker.database import db
            # Add all models here so that they register themselves to the db
            from tasker.home.models import User
            db.create_all()

    return app
