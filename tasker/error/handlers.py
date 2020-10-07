# 2020-09-30 20:02:39 -0700 - Emily Martens - add error handlers, templates for 404 and 500, and register blueprint - lines:,2,3,4,5,6,7,8,9,10,11,12,13,14
from flask import Blueprint, render_template
from tasker.models import db

bp = Blueprint('error', __name__, static_folder='../static')

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error/500.html'), 500
