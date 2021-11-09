from flask import Flask
from flask import *
#from . import db
import os
import sys
from flask_login import login_user, login_required, logout_user, current_user
from .database_handler import bookmark_channel, init, signup_user, user_login, User, change_pass
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from .auth import password_requirements

main = Blueprint('main',__name__)

@main.route('/home')
@login_required
def home():
    return render_template('Home.html')

@main.route('/search')
@login_required
def search():
    return render_template('Search.html')

@main.route('/stats')
@login_required
def stats():
    return render_template('Stats.html')

@main.route('/settings', methods = ['POST', 'GET'])
@login_required
def settings():
    if request.method == 'POST':
        # username = request.form['usrname']
        OldPass = request.form['oldpw']
        NewPass = request.form['newpw']
        user = User(None, current_user.username, None)
        password = user.hashedPassword
        flash('VALID password, everything up to now works!'+ str(OldPass) + str(NewPass) + str(current_user.username))
        if check_password_hash(password, OldPass):
             valid, error = password_requirements(NewPass)
             if valid:
                change_pass(user.username,NewPass)
             else:
                flash('Invalid NEW Password!', 'error')
        else:
            flash('Old password is not correct', 'error')
    return render_template('Settings.html')

# @main.route("/SettingPassChange", methods = ['POST'])


        


