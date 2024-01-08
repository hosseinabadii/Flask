from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy.orm import declarative_base

from config import Config

ROOT_PATH = Path(__file__).parent

csrf = CSRFProtect()
Base = declarative_base()
db = SQLAlchemy(model_class=Base)
mail = Mail()
from main.models import Post, User

login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


from admin.register import admin
from errors.handlers import errors
from main.views import main
from posts.views import posts
from users.views import users


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(posts, url_prefix="/posts")

    return app
