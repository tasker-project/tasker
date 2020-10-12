# 2020-10-03 21:26:31 -0400 - Jeremy Axmacher - Add task query and display based on view preference and timezone - lines:,15,16,20,22,23,31,32,38,70,71,75,79,80,81,82,83,84,85,87,88,89,90,91,92,93,129
# 2020-09-24 22:26:17 -0700 - Emily Martens - debug login_manager, add full login functionality, add logout route to menu - lines:,21,72,111,112
# 2020-10-03 10:59:59 -0400 - Jeremy Axmacher - Change view preference to dropdown nav - lines:,74,77,78
# 2020-09-19 13:07:50 -0700 - Emily Martens - add front end setup, blueprint setup for user, job_template - lines:,27,28,29,69,73
# 2020-09-27 13:28:53 -0700 - Emily Martens - fix naming discrepancies in user forms/views/templates, add form styling classes to register template, restructure login and register templates to match, re-enable User blueprint. - lines:,57,60,61,64,115
# 2020-10-10 13:53:35 -0700 - Emily Martens - change friendly_date_time to match Job Template formatting - lines:,33,34,35,36,37
# 2020-10-03 19:17:29 -0700 - Emily Martens - remove ChangeViewForm import from user/views - lines:,26
# 2020-09-25 21:56:01 -0400 - J Axmacher - Merge branch 'master' into Maged-user-register - lines:,17,108
# 2020-10-04 19:57:31 -0700 - Emily Martens - modify home view to filter out completed tasks. - lines:,25
# 2020-09-25 07:30:26 -0700 - Maged Bebawy - added user registeration - lines:,30,39,55,56,58,59,62,63,65,66,67,68,107
# 2020-09-24 21:54:21 -0700 - Emily Martens - add login setup, form, view, template, add logout route - lines:,18,24,109,110,113,114,116,118,119,121,122,123,124,125,126,127,128,130,131,132,133
# 2020-10-02 14:47:44 -0700 - Maged Bebawy - Updated flah messages and added sign link to the signup form - lines:,117,120
# 2020-10-02 21:34:11 -0400 - Jeremy Axmacher - Add view switching - lines:,19,76
# 2020-10-04 23:35:09 -0400 - Jeremy Axmacher - Slice home screen by past, current and future tasks - lines:,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,86,94,95,96,97,98,99,100,101,102,103,104,105,106
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
    day = starting_date.strftime('%B %d, %Y')
    time = int(starting_date.strftime('%I'))
    clock_time = starting_date.strftime('%p')
    date = day + " at " +  str(time) + " " + clock_time
    return date


def split_tasks(tasks, today):
    yeterday = today - 86400 # Seconds in a day
    past_due_tasks = []
    current_tasks = []
    future_tasks = []
    for task in tasks:
        if task.due_date <= yeterday:
            past_due_tasks.append(task)
        elif task.due_date <= today:
            current_tasks.append(task)
        else:
            future_tasks.append(task)
    return past_due_tasks, current_tasks, future_tasks


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
    today = int(timestamp.timestamp())
    # Add days depending on view
    if view == 'Week':
        timestamp = timestamp + datetime.timedelta(days=6)
    elif view == 'Month':
        timestamp = timestamp + datetime.timedelta(days=30)
    due_date = int(timestamp.timestamp())
    # Query for user's tasks with due dates less than calculated timestamp
    tasks = Task.query.\
        filter(
            Task.owner == current_user,
            Task.due_date <= due_date,
            Task.status != TaskStatus.Completed).\
        order_by(Task.due_date.asc())
    past_due_tasks, current_tasks, future_tasks = split_tasks(tasks, today)
    return render_template(
        'user/home.html', title="Home", view=view,
        views=views, past_due_tasks=past_due_tasks,
        current_tasks=current_tasks, future_tasks=future_tasks,
        user=current_user
    )


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
