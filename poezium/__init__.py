import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

from .models import User

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "connect_args": {"sslmode": "require"}
    }

    db.init_app(app)

    from .home import home_bp
    app.register_blueprint(home_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    # from .profile import profile_bp
    # app.register_blueprint(profile_bp)

    # from .search import search_bp
    # app.register_blueprint(search_bp)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app
