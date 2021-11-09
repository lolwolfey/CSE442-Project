from flask import *
#from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
#from .models import User
import sys
import psycopg2
import os
from .database_handler import bookmark_channel, init, signup_user, user_login, User, change_pass #delete when merging

auth = Blueprint('auth', __name__)


@auth.route("/")
def initialize():
    return redirect(url_for('auth.login'))


@auth.route("/login", methods =['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #bookmark_channel(1,username)#delete when merging
        user = User(None, username, password)
        
        if user.login(username, password):
            login_user(user, remember=True)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template("Login.html")


@auth.route("/SettingPassChange", methods = ['POST', 'GET'])
def SettingPassChange():
    if request.method == 'POST':
        username = request.form['usrname']
        OldPass = request.form['oldpw']
        NewPass = request.form['newpw']
        user = User(None, username, None)
        password = user.hashedPassword
        flash('VALID password, everything up to now works!')
        # if check_password_hash(password, OldPass):
        #     valid, error = password_requirements(NewPass)
        #     if valid:
                # change_pass(user.username,NewPass)
        #     else:
                # flash('VALID password, everything up to now works!', 'error')
        # else:
        #     flash('Old password is not correct', 'error')
    return render_template("Settings.html")
        

        

@auth.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        
        if password1 == password2:
            valid, error = password_requirements(password1)
            if valid:
                if signup_user(email, username, password1):
                    flash('Account created', 'info')
                    return redirect(url_for('auth.login'))
                else:
                    flash('That username/email address is already attached to an account.', 'error')
            else:
                for err in error:
                    flash(err, 'error')
        else:
            flash('Passwords do not match.', 'error')

    return render_template("Signup.html")

# The following Password requirements must be met:
# At least 8 characters long.
# 3 upper case letters.
# 3 lower case letters.
# 1 number.
# Returns a boolean valid parameter and a array of erros.
def password_requirements(password):
    count = 0
    upper_case = 0
    lower_case = 0
    number = 0
    valid = True
    error = []

    for char in password:
        count += 1
        if char.isupper():
            upper_case += 1
        elif char.islower():
            lower_case += 1
        elif char.isdigit():
            number += 1
    
    if count < 8:
        valid = False
        error.append('Must be at least 8 characters long.')
    if upper_case < 3:
        valid = False
        error.append('Must contain at least 3 capital letters.')
    if lower_case < 3:
        valid = False
        error.append('Must contain at least 3 lower case letters. ')
    if number < 1:
        valid = False
        error.append('Must contain at least 1 number.')

    if not valid:
        error.insert(0,'Invalid Password:')
    
    return valid, error



@auth.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

