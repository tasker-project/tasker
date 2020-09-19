from flask import Blueprint, render_template
from tasker.database import db
#from tasker.home.forms import LoginForm, RegistrationForm

bp = Blueprint('user', __name__, static_folder='../static')

@bp.route('/')

@bp.route('/home')
#@login_required
def home():
    user = {
    'username': 'test@testing.com', 'email' : 'test@testing.com', 'timezone' : 'EST', 'view' : 'Month'
    }
    view = "Month"
    dates = ['9.25.2020', '9.30.2020', '10.10.2020', '10.12.2020', '10.14.2020', '10.16.2020', '10.18.2020']
    return render_template('user/home.html', title="Home", dates=dates, user=user)
