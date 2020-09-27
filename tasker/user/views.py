from flask import Blueprint, render_template, redirect, request, url_for, flash

from werkzeug.urls import url_parse
from flask_login import current_user, login_user, login_required, logout_user
from tasker.app import bcrypt
from tasker.models import db, User
from tasker.user.forms import ChangeViewForm, SignInForm, SignUpForm

bp = Blueprint('user', __name__, static_folder='../static')



@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = SignUpForm()

    if form.validate_on_submit():
        if db.session.query(db.exists().where(User.email_address == form.email_address.data)).scalar():
            form.email_address.errors.append('Email already exists')
        else:
            user = User()
            user.create_user(form.email_address.data, form.password.data, form.timezone.data)
            flash('Successfully registered', 'success')
            return redirect(url_for('user.home'))
    return render_template('user/register.html', form=form)

@bp.route('/', methods=['GET', 'POST'])

@bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    user = {
    'username': 'test@testing.com', 'email' : 'test@testing.com', 'timezone' : 'EST', 'view' : 'Month'
    }
    templates = [
    {'id': 0, 'title':'Template 1', 'start_date' : '09.10.2020', 'interval': 3, 'interval_type' : 'Weeks', 'description' : 'Job Template description goes here.'},
    {'id': 1, 'title': 'Template 2', 'start_date' : '09.15.2020', 'interval': 5, 'interval_type' : 'Days', 'description' : 'Job Template description goes here.'},
    {'id' : 2, 'title':'Template 3', 'start_date' : '09.20.2020', 'interval' : 1, 'interval_type' : 'Months', 'description' : 'Job Template description goes here.'}
    ]
    tasks = [
    {'id' : 0, 'due_date' : '9.10.2020', 'template': templates[0]},
    {'id' : 1, 'due_date' : '9.20.2020', 'template': templates[1]},
    {'id' : 2, 'due_date' : '9.25.2020', 'template': templates[1]},
    {'id' : 3, 'due_date' : '9.30.2020', 'template': templates[1]},
    {'id' : 4, 'due_date' : '10.5.2020', 'template': templates[1]},
    {'id' : 5, 'due_date' : '10.5.2020', 'template': templates[2]},
    {'id' : 6, 'due_date' : '10.10.2020', 'template': templates[1]},
    ]
    form = ChangeViewForm()
    if form.validate_on_submit():
        view = form.select_view.data
        change_view = {'view': view}
        user.update(change_view)
        return render_template('user/home.html', title="Home", tasks=tasks, user=user, form=form)
    return render_template('user/home.html', title="Home", tasks=tasks, user=user, form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user is None:
            flash('Wrong username or password. Please try again.')
            return redirect(url_for('user.login'))
        if bcrypt.check_password_hash(user.password, form.password.data) == False:
            flash('Wrong username or password. Please try again.')
            return redirect(url_for('user.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user.home')
        return redirect(url_for('user.home'))
    return render_template('user/login.html', title="Login", form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login'))
