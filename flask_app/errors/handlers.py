from flask import Blueprint, render_template, redirect


errors_bp = Blueprint('errors_bp', __name__)

@errors_bp.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

# issue: 403 Error not rendering and crashing the site
@errors_bp.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors_bp.app_errorhandler(410)
def error_410(error):
    return render_template('errors/410.html'), 410

@errors_bp.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
