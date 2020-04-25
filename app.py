import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Task, Volunteer, setup_db

# create the app
app = Flask(__name__)
setup_db(app)
CORS(app)

# Routes
# Index route
@app.route('/')
def index():
    return {'success': True}

# Tasks routes ------------------------------------------------------------
@app.route('/tasks')
def get_tasks():
    tasks = Task.query.order_by('id').all()
    return {'tasks': [task.format() for task in tasks]}

@app.route('/tasks/<task_id>')
def get_task(task_id):
    task = Task.query.get(task_id)
    return task.format()

# Volunteers routes -------------------------------------------------------
@app.route('/volunteers')
def get_volunteers():
    volunteers = Volunteer.query.order_by('name').all()
    return {'volunteers': [vol.format() for vol in volunteers]}

@app.route('/volunteers/<vol_id>')
def get_volunteer(vol_id):
    volunteer = Volunteer.query.get(vol_id)
    return volunteer.format()




