from flask import Flask
from flask import *
from . import db
import os
import sys




#authenticated = [False]
#fake_database = []

main = Blueprint('main',__name__)

@main.route('/')
@login_required
def home():
    return render_template('testHome.html')



"""
if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)
    app.run(host='0.0.0.0', port=port, debug=True)
"""

