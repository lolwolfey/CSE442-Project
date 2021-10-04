from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os


db = SQLAlchemy()

def create_app():
    app=Flask(__name__)

    migrate = Migrate(app, db)

    app.config['SECRET_KEY'] = b'\nI\x18]\xc3\x96m&@\xbffG\xf5a.T'
    app.config['SQLALCHEMY_DATABSE_URI'] = os.environ['DATABASE_URL']

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login.manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Bluprints allow us to control the content users have access to. By creating a separate blueprint 
    # for authorization, we can remember which users are logged in and which are not.
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    

    #db.create_all()

    return app

