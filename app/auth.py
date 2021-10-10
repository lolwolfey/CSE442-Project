from flask import *
#from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
#from .models import User
import sys
import psycopg2
import os
from .database_handler import bookmark_channel, init, signup_user, login_user, User #delete when merging

auth = Blueprint('auth', __name__)

"""
@auth.route("/")
def initialize():
    #db.create_all()
    #RAW SQL
    init()
    return redirect(url_for('auth.login'))
"""


@auth.route("/login", methods =['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #bookmark_channel(1,username)#delete when merging
        """
        user = User.query.filter_by(username=username).first()

        
        if not user or not check_password_hash(user.password, password):
            flash('Invalid Ussername or Password. Try Again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        return redirect(url_for('main.home'))
        """
        user = User(username, password)
        if user.login(username, password):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.')

    return render_template("Login.html")


@auth.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        """
        if password1 == password2:

            # Check to see if email already exists.
            user = User.query.filter_by(email=email).first()
            if user:
                flash('That email already exists')
                return redirect(url_for('auth.signup'))
            user = User.query.filter_by(username=username).first()

            # check to see if username already exists.
            if user:
                flash('That username already exists')
                return redirect(url_for('auth.signup'))
            
            # If the user does not exist and the passwords match, a new user is created.
            new_user = User(email=email, 
                            username=username, 
                            password=generate_password_hash(password1, method='sha256')
                            )

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.login'))
        # Check to see if passwords match
        else:
            flash("Passwords do not match.")
            return redirect(url_for('auth.signup'))
        """
    if password1 == password2:
        if signup_user(email, username, password1):
            return redirect(url_for('auth.login'))
        else:
            flash('That username/email address is already attached to an account.')
    else:
        flash('Passwords do not match.')

    return render_template("Signup.html")

@auth.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

