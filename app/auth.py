from flask import *
#from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
#from .models import User
import sys
import psycopg2
import os
from .database_handler import bookmark_channel, init, signup_user, user_login, User, get_user_by_email, change_pass, confirm_reset_token, delete_reset_token #delete when merging

# """
# Reference Links
# --------------------------------------------------------------------------------------------------------------
# Werkzeug.security: https://werkzeug.palletsprojects.com/en/2.0.x/utils/
# flask: flask: https://flask.palletsprojects.com/en/2.0.x/
# flask message flashing: https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/ 
# flask-login: https://flask-login.readthedocs.io/en/latest/
# psycopg2: https://www.psycopg.org/docs/, https://www.psycopg.org/docs/cursor.html, https://www.psycopg.org/docs/connection.html
# sys: https://docs.python.org/3/library/sys.html
# os: https://docs.python.org/3/library/os.html
# """

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

#reset password using token for forgotten password (not logged in) version:
@auth.route('/reset_pw', methods = ['POST', 'GET'])
def SettingPassChange():
    if request.method == 'POST':
        useremail = request.form['user_email']
        token = request.form['reset_token']
        NewPass = request.form['new_pass']
        if confirm_reset_token(useremail, token) == True:
            valid, error = password_requirements(NewPass)
            if valid:
                userrow = get_user_by_email(useremail)
                username = userrow[2]
                change_pass(username, NewPass)
                delete_reset_token(useremail, token)
                flash('Password changed', 'info')
                return redirect(url_for('auth.login'))
            else:
                for err in error:
                    flash(err, 'error')
        else:
            flash('email or token is incorrect', 'error')
    return render_template('reset_password.html')

        

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
                email_req_check = email_requirements(email)
                if email_req_check == True:
                    if signup_user(email, username, password1):
                        flash('Account created', 'info')
                        return redirect(url_for('auth.login'))
                    else:
                        flash('That username/email address is already attached to an account.', 'error')
                else:
                    flash('Email is of invalid type, try again.', 'error')
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

#add email requirements
def email_requirements(email):
    if '@' in email and '.com' in email:
        return True
    else:
        return False


@auth.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

