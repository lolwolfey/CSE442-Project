from flask import Flask
from flask import *
#from . import db
import os
import sys
from flask_login import login_user, login_required, logout_user, current_user
from .database_handler import bookmark_channel, init, signup_user, user_login, User, change_pass, get_password_by_username
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
        # user = User(None, current_user.username, None)
        password = get_password_by_username(current_user.username)
        flash('VALID password, everything up to now works!'+ str(OldPass) + str(NewPass) + str(current_user.username))
        if check_password_hash(password, OldPass): #check if old password is correct
             valid, error = password_requirements(NewPass)  #check if new password meets requirements
             if valid:
                change_pass(current_user.username,NewPass)      #if it means requirements update password
             else:
                flash('Invalid NEW Password!', 'error')         #if not, generate error saying it did not
        else:
            flash('Old password is not correct', 'error')
    return render_template('Settings.html')

# @main.route("/SettingPassChange", methods = ['POST'])


        


