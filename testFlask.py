"""
How to deploy a Flask Application ith Docker:
https://www.digitalocean.com/community/tutorials/how-to-build-and-deploy-a-flask-application-using-docker-on-ubuntu-18-04

Flask basics:
https://flask.palletsprojects.com/en/2.0.x/quickstart/

Flask GitHub:
https://github.com/pallets/flask

Why use Flask:
Flask is super easy to understand even for people who have no experience with web applications. 
Routing is intuitive and framework has been well tested and integrated into other libraries.
I've worked with it before so will be able to offer guidence to any group members who need it.
"""

from flask import Flask
from flask import *
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("testHTML.html")