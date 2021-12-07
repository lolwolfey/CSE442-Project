from logging import DEBUG
from flask import Flask, request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import *
import os
from .database_handler import bookmark_channel, init, User, Check_email, generate_reset_token, confirm_reset_token, delete_reset_token
from flask_mail import Mail, Message

debug = True

def create_app():
    app=Flask(__name__)   

    app.config['SECRET_KEY'] = b'\nI\x18]\xc3\x96m&@\xbffG\xf5a.T'

    app.config.update(
        DEBUG = True,
        #email settings
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_Port = 587,
        MAIL_USE_SSL = False,
        MAIL_USE_TLS = True,
        MAIL_USERNAME = 'redlomansmurf125@gmail.com',
        MAIL_PASSWORD = 'wimjzfqkutwpclzt',
    )
    mail = Mail(app)

    @app.route('/send_mail', methods=['GET','POST'])
    def send_mail():
        if request.method == "POST":
            email = request.form['email']
            if Check_email(email) == True:
                message = Message(sender="redlomansmurf125@gmail.com", recipients=[email])
                token = generate_reset_token(email)
                message.body = "This is the reset token: " + token
                mail.send(message)
                return render_template("reset_password.html")
            else:
                flash('An error occured! Make sure your inputted email is correct and try again.', 'error')
        return render_template("Send_Email.html")

    # Initialize the ;login manager for Flask_login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # Initialize any tables that ar not already created.
    init()

    # Initializes a user based on their user_id. This is used in Flask_login to store the current_user variable.
    @login_manager.user_loader
    def load_user(user_id):
        user = User(user_id, None, None)
        return user

    # Bluprints allow us to control the content users have access to. By creating a separate blueprint 
    # for authorization, we can remember which users are logged in and which are not.
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

