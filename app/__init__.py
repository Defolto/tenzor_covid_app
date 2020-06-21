import os

from flask import Flask, g, session
from flask_login import LoginManager, current_user, login_required
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from app.models import User


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + app.instance_path + '/database.db'
    )
    global db
    db = SQLAlchemy(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)

    from . import stats
    app.register_blueprint(stats.bp)

    from . import user
    app.register_blueprint(user.bp)

    http_auth = HTTPBasicAuth()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Пожалуйста, войдите в свой аккаунт для продолжения"


    @login_manager.user_loader
    def user_loader(user_id):
        return db.session.query(User).filter(User.id == user_id).first()


    @app.before_request
    def user_setter():
        if '_user_id' in session:
            user = db.session.query(User).filter(User.id == session["_user_id"]).first()
            g.current_user = user

    @http_auth.verify_password
    def verify_pw(login, password):
        if not (login and password):
            return False
        u = get_session().query(User).filter(User.login == login).first()
        if u and u.check_password(password):
            g.current_user = u
            return True
        else:
            return False


    return app
