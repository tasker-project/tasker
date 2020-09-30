# 2020-09-10 17:51:11 -0400 - Jeremy Axmacher - Initial commit - lines:,3,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21
# 2020-09-23 23:09:41 -0400 - Jeremy Axmacher - Team collaborated on model schema definition - lines:,4
from flask import Blueprint, render_template
from tasker.models import db
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
