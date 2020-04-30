from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
import json


database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()


def setup_db(app, db_path=database_path):
    #  binds a flask application and an SQLAlchemy service
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    print('db path:', db_path)


'''
Task class
Contains the task title, details, date needed, status and, if status is not 
open, a volunteer id. A task will have at most 1 volunteer associated with it
'''


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=False)
    date_needed = db.Column(db.Date, nullable=False)
    status = db.Column(db.String, nullable=False, default='Open')
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'))
    volunteers = db.relationship('Volunteer',
                                 backref=db.backref(
                                     'volunteer_association',
                                     cascade='all, delete')
    )

    def __init__(self, title, details, date_needed, status=None):
        self.title = title
        self.details = details
        self.date_needed = date_needed
        self.status = status
        self.volunteer_id = None

    def format(self):
        vol_name = ''
        if self.volunteers:
            vol_name = self.volunteers.name
        return {
            'id': self.id,
            'title': self.title,
            'details': self.details,
            'date_needed': datetime.strftime(self.date_needed, '%Y-%m-%d'),
            'status': self.status,
            'volunteer_id': self.volunteer_id,
            'volunteer_name': vol_name
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


'''
Volunteer class
Contains the volunteer's name, address, phone number, and list of task ids 
that the volunteer has been assigned to. A volunteer may be assigned to
multiple tasks
'''


class Volunteer(db.Model):
    __tablename__ = 'volunteer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    tasks = db.relationship('Task',
                            backref=db.backref(
                                'task_association',
                                cascade='all, delete'))

    def __init__(self, name, address, city, state, zip_code, phone_number):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone_number = phone_number

    def format(self):
        task_list = Task.query.filter_by(volunteer_id=self.id).all()
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'phone_number': self.phone_number,
            'tasks': [task.format() for task in task_list]
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
