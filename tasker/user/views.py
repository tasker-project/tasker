import time
import datetime

from werkzeug.urls import url_parse
from werkzeug.exceptions import NotFound
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from pytz import timezone

from tasker.app import bcrypt
from tasker.models import db, User, Task, TaskStatus
from tasker.user.forms import SignInForm, SignUpForm

bp = Blueprint('user', __name__, static_folder='../static')


def friendly_date_time(d):
    starting_date = datetime.datetime.fromtimestamp(d, tz=timezone(current_user.timezone))
    return starting_date.strftime('%B %d, %Y %I:%M %p')


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


@bp.route('/')
@bp.route('/home')
@login_required
def home():
    views = ('Day', 'Week', 'Month')
    # Get the current view preference from querystring
    view = request.args.get('view', 'Day')
    if view not in views:
        return redirect(url_for('user.home'))
    # Get current time
    now = int(time.time())
    tz = timezone(current_user.timezone)
    # Convert to user's timezone and shift to the end of current calendar day
    timestamp = datetime.datetime.\
        fromtimestamp(now, tz=tz).\
        replace(hour=23, minute=59, second=59)
    # Add days depending on view
    if view == 'Week':
        timestamp = timestamp + datetime.timedelta(days=6)
    elif view == 'Month':
        timestamp = timestamp + datetime.timedelta(days=30)
    due_date = int(timestamp.timestamp())
    # Query for user's tasks with due dates less than calculated timestamp
    tasks = Task.query.filter(Task.owner == current_user, Task.due_date <= due_date, Task.status != TaskStatus.Completed)
    return render_template('user/home.html', title="Home", view=view, views=views, tasks=tasks, user=current_user)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user is None:
            flash('Wrong username or password. Please try again.', 'error')
            return redirect(url_for('user.login'))
        if bcrypt.check_password_hash(user.password, form.password.data) == False:
            flash('Wrong username or password. Please try again.', 'error')
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
