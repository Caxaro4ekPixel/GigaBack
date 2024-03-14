from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_authorize import Authorize
from flask_praetorian import Praetorian
from password_validation import PasswordPolicy
from importlib import import_module

db = SQLAlchemy()
authorize = Authorize()
guard = Praetorian()
policy = PasswordPolicy()
login_manager = LoginManager()


def create_app(app_config):
    app = Flask(__name__)
    app.config.from_object(app_config)
    db.init_app(app)

    from app.database.models import Users

    from .src.auth import auth as auth_blueprint
    import_module('app.src.auth.router')
    app.register_blueprint(auth_blueprint)

    with app.app_context():
        guard.init_app(app, user_class=Users)
        login_manager.login_view = 'auth.login'

        @login_manager.user_loader
        def load_user(user_id):
            return Users.query.get(int(user_id))

        db.create_all()

    return app
