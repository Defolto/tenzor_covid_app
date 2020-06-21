from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_login import login_required


bp = Blueprint('stats', __name__)


@bp.route('/index', methods=('GET',))
def index():
    return render_template('stats/index.html')
