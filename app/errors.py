from flask import Blueprint, render_template
from werkzeug.exceptions import HTTPException

bp = Blueprint('error', __name__)

@bp.app_errorhandler(HTTPException)
def handle_http_exception(e):
    """Error handler for http errors"""
    print(e)
    return render_template('http_error.html', e=e)

@bp.app_errorhandler(Exception)
def handle_generic_exception(e):
    """Error handler for all errors"""
    print(e)
    return render_template('generic_error.html', e=e), 500
