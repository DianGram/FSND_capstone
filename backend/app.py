import sys
from flask import Flask, request, abort, jsonify
from .models import Task, Volunteer, setup_db
from .auth import AuthError, requires_auth

def create_app():
    # create the app
    app = Flask(__name__)
    setup_db(app)

    # Routes
    # Index route
    @app.route('/')
    def index():
        return {'success': True}

    # Tasks routes ------------------------------------------------------------
    @app.route('/tasks')
    def get_tasks():
        # returns a list of all tasks
        tasks = Task.query.order_by('id').all()
        if not tasks:
            abort(404)
        return {
            'success': True,
            'tasks': [task.format() for task in tasks]}

    @app.route('/tasks/<int:task_id>')
    def get_task(task_id):
        # returns the task having id = task_id
        task = Task.query.get(task_id)
        if not task:
            abort(404)

        return {
            'success': True,
            'task': task.format()
        }

    @app.route('/tasks/<int:task_id>', methods=['PATCH'])
    @requires_auth('patch:task')
    def update_task(token, task_id):
        # updates the task having id = task_id and returns the updated task
        task = Task.query.get(task_id)
        if not task:
            abort(404)

        body = request.get_json()
        if not body:
            abort(400)

        # only fields being updated will be in the body, so keep current
        # value for all others
        task.title = body.get('title', task.title)
        task.details = body.get('details', task.details)
        task.date_needed = body.get('date_needed', task.date_needed)
        task.status = body.get('status', task.status)
        task.volunteer_id = body.get('volunteer_id', task.volunteer_id)

        try:
            task.update()
        except Exception:
            print('422 Error', sys.exc_info())
            abort(422)

        return {
            'success': True,
            'task': task.format()
        }

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    @requires_auth('delete:task')
    def delete_task(token, task_id):
        # deletes the task having id = task_id and returns the task id
        task = Task.query.get(task_id)
        if not task:
            abort(404)

        try:
            task.delete()
        except Exception:
            print('422 Error', sys.exc_info())
            abort(422)

        return {
            'success': True,
            'deleted': task_id
        }

    @app.route('/tasks/create', methods=['POST'])
    @requires_auth('post:task')
    def create_task(token):
        # creates a new task and returns it
        body = request.get_json()
        if not body:
            abort(400)

        title = body.get('title', None)
        details = body.get('details', None)
        date_needed = body.get('date_needed', None)
        status = body.get('status', 'Open')
        if title and details and date_needed:
            try:
                new_task = Task(title, details, date_needed, status)
                new_task.insert()
                return {'success': True,
                        'task': new_task.format()
                        }
            except Exception:
                print('422 Error', sys.exc_info())
                abort(422)
        else:
            # request did not contain one or more required fields
            abort(400)

    # Volunteers routes -------------------------------------------------------
    @app.route('/volunteers')
    @requires_auth('get:volunteer')
    def get_volunteers(token):
        # returns all volunteers
        volunteers = Volunteer.query.order_by('name').all()
        return {'success': True,
                'volunteers': [vol.format() for vol in volunteers]
                }

    @app.route('/volunteers/<int:vol_id>')
    @requires_auth('get:volunteer')
    def get_volunteer(token, vol_id):
        # returns the volunteer whose id = vol_id
        volunteer = Volunteer.query.get(vol_id)
        if not volunteer:
            abort(404)
        return {
            'success': True,
            'volunteer': volunteer.format()
        }

    @app.route('/volunteers/<int:vol_id>', methods=['PATCH'])
    @requires_auth('patch:volunteer')
    def update_volunteer(token, vol_id):
        # updates the volunteer having id = vol_id and returns the updated
        # volunteer
        volunteer = Volunteer.query.get(vol_id)
        if not volunteer:
            abort(404)

        body = request.get_json()
        if not body:
            abort(400)

        volunteer.name = body.get('name', volunteer.name)
        volunteer.address = body.get('address', volunteer.address)
        volunteer.city = body.get('city', volunteer.city)
        volunteer.state = body.get('state', volunteer.state)
        volunteer.zip_code = body.get('zip_code', volunteer.zip_code)
        volunteer.phone_number = body.get('phone_number', volunteer.phone_number)

        try:
            volunteer.update()
        except Exception:
            abort(422)

        return {
            'success': True,
            'volunteer': volunteer.format()
        }

    @app.route('/volunteers/<int:vol_id>', methods=['DELETE'])
    @requires_auth('delete:volunteer')
    def delete_volunteer(token, vol_id):
        # deletes the volunteer having id = vol_id and returns the vol_id
        volunteer = Volunteer.query.get(vol_id)
        if not volunteer:
            abort(404)

        try:
            volunteer.delete()
        except Exception:
            abort(422)

        return {
            'success': True,
            'deleted': vol_id
        }

    @app.route('/volunteers/create', methods=['POST'])
    @requires_auth('post:volunteer')
    def create_volunteer(token):
        # creates a new volunteer and returns it
        body = request.get_json()
        if not body:
            abort(400)

        name = body.get('name', None)
        address = body.get('address', None)
        city = body.get('city', None)
        state = body.get('state', None)
        zip_code = body.get('zip_code', None)
        phone_number = body.get('phone_number', None)
        # all fields are required
        if name and address and city and state and zip_code and phone_number:
            try:
                new_volunteer = Volunteer(name, address, city, state, zip_code, phone_number)
                new_volunteer.insert()
                return {
                    'success': True,
                    'volunteer': new_volunteer.format()
                }
            except Exception:
                abort(422)
        else:
            # request did not contain one or more required fields
            abort(400)

    # Error Handlers ----------------------------------------------------------
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Method Not Allowed"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Uprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return {
                   "success": False,
                   "error": "Authentication Error",
                   "message": error.error['code'] + ' - ' + error.error['description']
               }, 401

    return app


app = create_app()
