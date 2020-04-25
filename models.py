from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, db_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()

    # with app.app_context():
    #     db.create_all()


'''
Task class
Contains the task title, details and date needed
'''


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    details = db.Column(db.String)
    date_needed = db.Column(db.Date)

    def __init__(self, title, details, date_needed):
        self.title = title
        self.details = details
        self.date_needed = date_needed

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'details': self.details,
            'date_needed': self.date_needed}


'''
Volunteer class
Contains the volunteer's name, address, and phone number
'''


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    phone_number = db.Column(db.String(12))

    def __init__(self, name, address, city, state, zip_code, phone_number):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone_number = phone_number

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone_number': self.phone_number
        }
