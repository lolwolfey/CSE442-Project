from flask import Flask
from flask import *
#from . import db
import os
import sys
from flask_login import login_user, login_required, logout_user, current_user

main = Blueprint('main',__name__)

@main.route('/home')
@login_required
def home():
    return render_template('testHome.html')

@main.route('/search')
@login_required
def search():
    return render_template('Search.html')

@main.route('/stats')
@login_required
def stats():
    return render_template('Stats.html')

@main.route('/settings')
@login_required
def settings():
    return render_template('Settings.html')




