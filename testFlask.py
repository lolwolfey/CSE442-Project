from flask import Flask
from flask import *
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("testHTML.html")