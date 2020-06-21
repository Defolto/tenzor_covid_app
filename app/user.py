from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/user_page', methods=('GET',))
@login_required
def user_page():
    return render_template('user/user.html')
