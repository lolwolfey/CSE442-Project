from . import db 

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    def __init__(self, name, model, doors):
        self.name = name
        self.model = model
        self.doors = doors