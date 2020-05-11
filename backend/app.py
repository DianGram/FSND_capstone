import sys
import os
import json
from flask import Flask, request, abort, jsonify, render_template, session, \
    redirect, flash
from models import Task, Volunteer, setup_db
from forms import TaskForm, VolunteerForm
from auth import AuthError, requires_auth
from authlib.integrations.flask_client import OAuth

def create_app():
    # create the app
    static_folder = os.path.abspath('../frontend/static')
    app = Flask(__name__, template_folder='../frontend/templates', static_folder=static_folder)
    setup_db(app)

    auth0_domain = os.environ.get('AUTH0_DOMAIN')
    auth0_base_url = 'https://' + auth0_domain
    audience = os.environ.get('API_AUDIENCE')
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    redirect_url = os.environ.get('REDIRECT_URL')

    app.secret_key = client_secret

    oauth = OAuth(app)
    auth0 = oauth.register(
        'auth0',
        client_id=client_id,
        client_secret=client_secret,
        api_base_url=auth0_base_url,
        access_token_url=auth0_base_url + '/oauth/token',
        authorize_url=auth0_base_url + '/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )
    print('api_base_url', auth0_base_url)
    print('access_token_url', auth0_base_url + '/oauth/token')
    print('authorize_url', auth0_base_url + '/authorize')

    # Routes
    # Index route
    @app.route('/')
    def index():
        print('index')
        # return {'success': True}
        return render_template('home.html')

    # Login route
    @app.route('/login')
    def login():
        # print('/login')
        # print('auth0_domain', auth0_domain)
        # print('algorithms', algorithms)
        # print('audience', audience)
        # print('client_id', client_id)
        # print('redirect_url', redirect_url)
        return auth0.authorize_redirect(redirect_uri=redirect_url, audience=audience)

    @app.route('/callback')
    def auth0_callback_handling():
        response = auth0.authorize_access_token()
        token = response.get('access_token')
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        session['return_html'] = True
        session['jwt_token'] = token
        session['user'] = {
            'user_id': userinfo['sub'],
            'email': userinfo['email'],
            'first_name': userinfo['nickname'].title(),
        }
        return redirect('/dashboard')

    @app.route('/dashboard')
    @requires_auth('get:volunteer')
    def dashboard():
        return render_template('dashboard.html',
                               userinfo=session['user'],
                               userinfo_pretty=session['jwt_token'])

    # Tasks routes ------------------------------------------------------------
    @app.route('/tasks')
    def get_tasks():
        # returns a list of all tasks
        tasks = Task.query.order_by('id').all()
        # print('request headers', request.headers)
        # print('request environ', request.environ)
        # print('request url root', request.url_root)
        # print('request get json', request.get_json())
        if not tasks:
            abort(404)

        formatted_tasks = [task.format() for task in tasks]
        if session.get('return_html', False):
            return render_template('task_list.html', tasks=formatted_tasks)
        else:
            return {
                'success': True,
                'tasks': formatted_tasks
            }

    @app.route('/tasks/<int:task_id>')
    def get_task(task_id):
        # returns the task having id = task_id
        task = Task.query.get(task_id)
        if not task:
            abort(404)

        if session.get('return_html', False):
            return render_template('show_task.html', task=task.format())
        else:
            return {
                'success': True,
                'tasks': task.format()
            }

    @app.route('/tasks/search', methods=['POST'])
    def search_tasks():
        search_term = request.form.get('search_term', '')
        tasks = Task.query.filter(Task.title.ilike('%{}%'.format(search_term))).all()
        if not tasks:
            print('No tasks found')
            flash('No tasks match "' + search_term + '"')
            return redirect('/dashboard')

        return render_template('task_list.html', tasks=[task.format() for task in tasks])

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

    @app.route('/tasks/add', methods=['GET'])
    @requires_auth('post:task')
    def add_task_form():
        form = TaskForm()
        return render_template('task_form.html', form=form)

    @app.route('/tasks/add', methods=['POST'])
    @requires_auth('post:task')
    def add_task_submission(token=None):
        form = TaskForm()
        if not form.validate_on_submit():
            flash('Task could not be created because one or more data fields'
                  ' were invalid:')
            for field, message in form.errors.items():
                flash(message[0])
            return render_template('task_form.html', form=form)

        # the form is valid
        title = request.form['title']
        details = request.form['details']
        date_needed = request.form['date_needed']
        status = request.form['status']

        new_task = Task(title, details, date_needed, status)
        try:
            new_task.insert()
            flash('Task ' + title + ' was successfully created')
        except Exception as e:
            print('Error!', sys.exc_info())
            flash('An error occurred.  The Task could not be created')
            abort(422)

        return redirect('/dashboard')

    # Volunteers routes -------------------------------------------------------
    @app.route('/volunteers')
    @requires_auth('get:volunteer')
    def get_volunteers():
        # returns all volunteers
        print('/volunteers')
        volunteers = Volunteer.query.order_by('name').all()
        print('volunteer', volunteers[0])
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

    @app.route('/volunteers/search', methods=['POST'])
    def search_volunteers():
        search_term = request.form.get('search_term', '')
        volunteers = Volunteer.query.filter(Volunteer.name.ilike('%{}%'.format(search_term))).all()

        if not volunteers:
            print('No volunteers found')
            flash('No volunteers match "' + search_term + '"')
            return redirect('/dashboard')

        return render_template('volunteer_list.html', volunteers=[vol.format() for vol in volunteers])

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

    @app.route('/volunteers/add', methods=['GET'])
    @requires_auth('post:volunteer')
    def add_volunteer_form():
        form = VolunteerForm()
        return render_template('volunteer_form.html', form=form)

    @app.route('/volunteers/add', methods=['POST'])
    @requires_auth('post:volunteer')
    def add_volunteer_submission():
        form = VolunteerForm()
        if not form.validate_on_submit():
            print('form is not valid')
            flash('Task could not be created because one or more data fields'
                  ' were invalid:')
            for field, message in form.errors.items():
                flash(message[0])
                print('Error :', field, message[0])
            return render_template('volunteer_form.html', form=form)

        # the form is valid
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        phone_number = request.form['phone_number']

        new_volunteer = Volunteer(name, address, city, state, zip_code, phone_number)
        try:
            new_volunteer.insert()
            flash('Volunteer ' + name + ' was successfully added')
        except Exception as e:
            print('Error!', sys.exc_info())
            flash('An error occurred.  The Volunteer could not be added')
            abort(422)

        return redirect('/dashboard')

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

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return {
                   "success": False,
                   "error": "Authentication Error",
                   "message": error.error['code'] + ' - ' + error.error['description']
               }, 401

    return app


app = create_app()
