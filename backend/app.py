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
        return render_template('home.html')

    # Login route
    @app.route('/login')
    def login():
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
    # @requires_auth('get:volunteer')
    def dashboard():
        # if user is not logged in, they are not authorized for this route
        # so send them to the / route
        if session.get('jwt_token', False):
            return render_template('dashboard.html',
                                   userinfo=session['user'],
                                   userinfo_pretty=session['jwt_token'])
        else:
            return redirect('/')

    # Tasks routes ------------------------------------------------------------
    @app.route('/tasks')
    def get_tasks():
        # returns a list of all tasks
        tasks = Task.query.order_by('id').all()
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

    @app.route('/tasks/open')
    def get_open_tasks():
        # returns a list of all tasks with status of 'Open'
        tasks = Task.query.filter(Task.status == 'Open').order_by(Task.id).all()
        formatted_tasks = [task.format() for task in tasks]
        return render_template('task_list.html', tasks=formatted_tasks)

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
        # returns a list of all tasks whose title contains the search term
        search_term = request.form.get('search_term', '')
        tasks = Task.query.filter(Task.title.ilike('%{}%'.format(search_term))).all()
        if not tasks:
            flash('No tasks match "' + search_term + '"')
            return redirect('/dashboard')

        return render_template('task_list.html', tasks=[task.format() for task in tasks])

    @app.route('/tasks/update/<int:task_id>', methods=['GET'])
    @requires_auth('patch:task')
    def update_task_form(task_id):
        # sends the task_form.html page with action of "Update"
        task = Task.query.get(task_id)
        form = TaskForm(obj=task)

        # get all volunteers in name order for volunteer choices in form
        volunteers = Volunteer.query.order_by('name').all()
        print('id:', volunteers[0].id, 'name:', volunteers[0].name)
        form.volunteer_id.choices = [(v.id, v.name) for v in volunteers]
        for a, b in form.volunteer_id.choices:
            print(a, ':', b)
        return render_template('task_form.html', form=form, task=task, title="Update Task")

    @app.route('/tasks/update/<int:task_id>', methods=['POST'])
    @requires_auth('patch:task')
    def update_task_submission(task_id):
        # updates the task having id = task_id and returns the updated task to the gui
        form = TaskForm()

        volunteers = Volunteer.query.order_by('name').all()
        print('id:', volunteers[0].id, 'name:', volunteers[0].name)
        form.volunteer_id.choices = [(v.id, v.name) for v in volunteers]

        if not form.validate_on_submit():
            print("form not valid")
            flash('Task ' + request.form['title'] + ' could not be updated be'
                                                    'cause one or more fields'
                                                    ' were invalid:')
            for field, message in form.errors.items():
                flash(message[0])
            task = form.data
            task['id'] = task_id
            return render_template('task_form.html', form=form, task=task, title="Update Task")

        # form is valid
        print('form is valid', form)
        try:
            task=Task.query.get(task_id)
            form=TaskForm(ojb=task)
            form.populate_obj(task)
            task.update()
        except Exception as e:
            flash('Task ' + request.form['title'] + ' could not be updated')
            abort(422)

        flash('Task ' + task.title + ' was successfully updated')
        return redirect('/tasks')

    @app.route('/tasks/<int:task_id>', methods=['PATCH'])
    @requires_auth('patch:task')
    def patch_task(task_id):
        # updates the task having id = task_id and returns the updated task to the api
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

    # @app.route('/tasks/delete/<int:task_id>', methods=['POST'])
    # @requires_auth('delete:task')
    # def delete_task(task_id):
    #     task = Task.query.get(task_id)
    #     if not task:
    #         flash('Task ' + task.title + ' was not found')
    #         abort(404)
    #
    #     try:
    #         task.delete()
    #     except Exception as e:
    #         print('422 Error  ', sys.exc_info())
    #         flash('Task "' + task.title + '" could not be deleted')
    #         abort(422)
    #
    #     flash('Task "' + task.title + '" was successfully deleted')
    #     return redirect('/tasks')

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    @requires_auth('delete:task')
    def delete_task(task_id):
        # deletes the task having id = task_id and returns the task id
        task = Task.query.get(task_id)
        if not task:
            flash('Task ' + task.title + ' was not found')
            abort(404)

        try:
            task.delete()
        except Exception:
            print('422 Error', sys.exc_info())
            abort(422)

        flash('Task "' + task.title + '" was successfully deleted')
        return {
            'success': True,
            'deleted': task_id
        }

    @app.route('/tasks/create', methods=['POST'])
    @requires_auth('post:task')
    def create_task_api():
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
        return render_template('task_form.html', form=form, title="Add a New Task")

    @app.route('/tasks/add', methods=['POST'])
    @requires_auth('post:task')
    def add_task_submission():
        form = TaskForm()
        if not form.validate_on_submit():
            flash('Task could not be created because one or more data fields'
                  ' were invalid:')
            for field, message in form.errors.items():
                flash(message[0])
            return render_template('task_form.html', form=form, title="Add a New Task")

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
        # returns a list of all volunteers
        volunteers = Volunteer.query.order_by('name').all()

        if session.get('return_html', False):
            return render_template('volunteer_list.html', volunteers=[v.format() for v in volunteers])
        else:
            return {'success': True,
                    'volunteers': [vol.format() for vol in volunteers]
                    }

    @app.route('/volunteers/<int:vol_id>')
    @requires_auth('get:volunteer')
    def get_volunteer(vol_id):
        # returns the volunteer whose id = vol_id
        volunteer = Volunteer.query.get(vol_id)
        if not volunteer:
            abort(404)

        if session.get('return_html', False):
            return render_template('show_volunteer.html', volunteer=volunteer.format())
        else:
            return {
                'success': True,
                'volunteer': volunteer.format()
            }

    @app.route('/volunteers/search', methods=['POST'])
    def search_volunteers():
        # returns a list of all volunteers whose name contains the search term - gui only
        search_term = request.form.get('search_term', '')
        volunteers = Volunteer.query.filter(Volunteer.name.ilike('%{}%'.format(search_term))).all()

        if not volunteers:
            print('No volunteers found')
            flash('No volunteers match "' + search_term + '"')
            return redirect('/dashboard')

        return render_template('volunteer_list.html',
                               volunteers=[vol.format() for vol in volunteers])

    @app.route('/volunteers/update/<int:vol_id>', methods=['GET'])
    @requires_auth('patch:volunteer')
    def update_volunteer_form(vol_id):
        # sends the volunteer_form.html page"
        volunteer = Volunteer.query.get(vol_id)
        form = VolunteerForm(obj=volunteer)

        return render_template('volunteer_form.html',
                               form=form,
                               volunteer=volunteer,
                               title="Update Volunteer")

    @app.route('/volunteers/update/<int:vol_id>', methods=['POST'])
    @requires_auth('patch:volunteer')
    def update_volunteer_submission(vol_id):
        # updates the volunteer having id = vol_id and returns the updated
        # volunteer to the gui.  Use route /volunteers/vol_id method=PATCH to
        # return the volunteer to the api
        form = VolunteerForm()

        if not form.validate_on_submit():
            flash('Volunteer ' + request.form['name'] + ' could not be updated'
                                                        ' because one or more '
                                                        'fields were invalid:')
            for field, message in form.errors.items():
                flash(message[0])
            volunteer = form.data
            volunteer['id'] = vol_id
            return render_template('volunteer_form.html',
                                   form=form,
                                   volunteer=volunteer,
                                   title="Update Volunteer")

        # form is valid
        print('form is valid', form)
        try:
            volunteer=Volunteer.query.get(vol_id)
            form=VolunteerForm(ojb=volunteer)
            form.populate_obj(volunteer)
            volunteer.update()
        except Exception as e:
            flash('Volunteer ' + request.form['name'] + ' could not be updated')
            abort(422)

        flash('Volunteer ' + volunteer.name + ' was successfully updated')
        return redirect('/volunteers')


    @app.route('/volunteers/<int:vol_id>', methods=['PATCH'])
    @requires_auth('patch:volunteer')
    def update_volunteer(vol_id):
        # updates the volunteer having id = vol_id and returns the updated
        # volunteer to the api.  Use route /volunteers/update/vol_id to
        # return the volunteer to the gui
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
    def delete_volunteer(vol_id):
        # deletes the volunteer having id = vol_id and returns the vol_id
        volunteer = Volunteer.query.get(vol_id)
        if not volunteer:
            abort(404)

        try:
            volunteer.delete()
        except Exception:
            abort(422)

        flash('Volunteer ' + volunteer.name + ' was successfully deleted')
        return {
            'success': True,
            'deleted': vol_id
        }

    @app.route('/volunteers/create', methods=['POST'])
    @requires_auth('post:volunteer')
    def create_volunteer():
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
        return render_template('volunteer_form.html', form=form, title="Add a New Volunteer")

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
            return render_template('volunteer_form.html', form=form, title="Add a New Volunteer")

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
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

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
