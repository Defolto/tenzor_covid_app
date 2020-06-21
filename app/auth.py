from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_user, logout_user

from app import db
from app.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        error = None

        if not login:
            error = 'Введите логин'
        elif not password:
            error = 'Введите пароль'
        elif db.session.query(User)\
                       .filter(User.login == login)\
                       .first() is not None:
            error = 'Пользователь {} уже зарегистрирован'.format(login)

        if error is None:
            u = User(login=login)
            u.hash_password(password)
            db.session.add(u)
            db.session.commit()
            login_user(u)
            return redirect(url_for('stats.index'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        error = None

        u = db.session.query(User).filter(User.login == login).first()

        if u is None:
            error = 'Неверный логин'
        elif not u.check_password(password):
            error = 'Неверный пароль'

        if error is None:
            session.clear()
            login_user(u)
            return redirect(url_for('stats.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('stats.index'))
