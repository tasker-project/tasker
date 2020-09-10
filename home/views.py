from flask import Blueprint, render_template
from tasker.database import db
from tasker.home.forms import MyForm
from tasker.home.models import User

blueprint = Blueprint('home', __name__, static_folder='../static')


@blueprint.route('/', methods=('GET', 'POST'))
def index():
    form = MyForm()
    if form.validate_on_submit():
        user = User(name=form.name.data)
        db.session.add(user)
        db.session.commit()
        users = User.query.all()
        return render_template('index.jinja2', form=form, message='Just saved!', users=users)
    users = User.query.all()
    return render_template('index.jinja2', form=form, users=users)