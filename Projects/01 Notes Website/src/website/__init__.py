from flask import Flask
from flask_login import LoginManager

from .auth import auth
from .database import SQLALCHEMY_DATABASE_URL, db_session, init_db
from .models import User
from .views import views


def create_app():
    app = Flask(__name__)
    app.config[
        "SECRET_KEY"
    ] = "28287392a914eb5da6e212122c9d1167851427b8320eb151dff2af68bb63c730"
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return db_session.get(User, int(id))

    return app
