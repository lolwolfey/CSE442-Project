from flask_login import UserMixin
from . import db 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
