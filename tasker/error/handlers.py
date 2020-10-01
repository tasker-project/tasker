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
