# Feed the Kids  Backend

## Getting Started

This app can be run either locally, at http://localhost:5000, or on heroku, at https://for-the-kids.herokuapp.com/
The following instructions apply only if you want to run locally.  To run on heroku, simply navigate to https://for-the-kids.herokuapp.com/


### Installing Dependencies

#### Python 3
If you don't already have Python 3 installed on your computer, follow the instructions to install the latest version for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


#### Virtual Environment
Set up a Virtual Environment for this project
```bash
$ python3 -m venv udacity_env   
$ source udacity_env/bin/activate
```
A virtual environment named udacity_env will automatically activate when running
setup.sh.  If you choose to name your venv differently, you will need to change the 
name in the setup.sh file to your chosen name.

#### PIP Install Dependencies
Once you have your virtual environment set up and running, install dependencies by navigating to the /backend directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages listed in the requirements.txt file.


##### Key Dependencies
- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. It is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM that will handle the postgreSQL database. 

- [python-jose](https://python-jose.readthedocs.io/en/latest/) is a JavaScript Object Signing and Encryption technology used to decode and validate jwt (JSON Web Tokens)


## Database Setup
You'll need to create a database before running the app:
```bash
$ createdb capstone
```
Now run the following to create the tables for the database:
```bash
$ python3 manage.py db init
$ python3 manage.py db migrate
$ python3 manage.py db upgrade
```


## Running the server
Run the following from within the backend directory:
```bash
$ source setup.sh
$ flask run
```
This will activate the virtual environment, set the necessary environment variables and start the flask server.  
 In your browser, navigate to http://localhost:5000


## Testing
In order to run the unittests, you will need to setup the test database. If you are not already in your virtual environment, navigate to the /backend folder and follow the instructions above for Running the Server, then run:
```bash
$ dropdb ftk_test
$ createdb ftk_test
$ psql ftk_test < ftk_test.psql
```
Once the test database is set up, you can run the unittests:
```bash
$ source run_unittests.sh
```

If the reviewer wants to test the API by using curl, for your convenience there are
environment variables set up with tokens that are valid for 24 hours from submission
of the project.  The environment variables are ASSISTANT_TOKEN and DIRECTOR_TOKEN.
The unittests use these same environment variables to test RBAC.


# API Reference
## Getting Started
Feed the Kids is hosted at https://for-the-kids.herokuapp.com
It can also be run locally at http://localhost:5000

## Endpoints
Note: most endpoints require authentication.  
All endpoints will return a success value.

GET /tasks
- Gets all tasks
- Permission required: None
- Returns: A dictionary containing a list of all tasks
- Sample: `curl http://localhost:5000/tasks`
- Response:
```
{
  "success": true,
  "tasks": [
    {
      "date_needed": "2020-04-27",
      "details": "Publix address: 123 Main St, OurTown",
      "id": 1,
      "status": "Open",
      "title": "Pick up donations - Publix",
      "volunteer_id": 1,
      "volunteer_name": "Joan Smith"
    },
    {
      "date_needed": "2020-05-01",
      "details": "Make 3 dozen ham and cheese sandwiches",
      "id": 2,
      "status": "Open",
      "title": "Make Sandwiches",
      "volunteer_id": 2,
      "volunteer_name": "Jim Bob Jones"
    }
  ]
}
```

GET /tasks/{int:task_id}
- Gets information about a particular task
- Permission required: None
- Returns: A dictionary containing a task object whose id matches the requested task_id
- Sample: `curl http://localhost:5000/tasks/1`
- Response:
```
{
  "success": true,
  "task": {
    "date_needed": "2020-04-27",
    "details": "Publix address: 123 Main St, OurTown",
    "id": 1,
    "status": "Open",
    "title": "Pick up donations - Publix",
    "volunteer_id": 1,
    "volunteer_name": "Joan Smith"
  }
}
```

POST /tasks/create
- Creates a new task with the given data
- Permission required: post:task
- Required data: title, details, date_needed, status
- Returns: The task object that was created 
- Sample: 
```
curl --request POST 'http://localhost:5000/tasks/create' \
--header 'Authorization: Bearer {your_access_token} \
--header 'Content-Type: application/json' \
--data-raw '{
	"title": "Deliver meals to YMCA",
	"details": "Deliver meals to the YMCA at 123 Main St. Ourtown by Noon",
	"date_needed": "2020-05-05",
	"status": "Open"
}'
```
- Response:
```
{
  "success": true,
  "task": {
    "date_needed": "2020-05-05",
    "details": "Deliver meals to the YMCA at 123 Main St. Ourtown by Noon",
    "id": 49,
    "status": "Open",
    "title": "Deliver meals to YMCA",
    "volunteer_id": null,
    "volunteer_name": ""
  }
}
```

PATCH /tasks/{int:task_id}
- Updates the task having the requested task_id with the given data.  
- Permission required: patch:task
- Required data:  Only the fields to be updated should be included
- Returns: The updated task object 
- Sample: 
```
curl --request PATCH 'http://localhost:5000/tasks/2' \
--header 'Authorization: Bearer {your_access_token} \
--header 'Content-Type: application/json' \
--data-raw '{
	"status": "Complete"
}'
```
- Response:
```
{
  "success": true,
  "task": {
    "date_needed": "2020-05-01",
    "details": "Make 3 dozen ham and cheese sandwiches",
    "id": 2,
    "status": "Complete",
    "title": "Make Sandwiches",
    "volunteer_id": 2,
    "volunteer_name": "Jim Bob Jones"
  }
}
```

DELETE /tasks/{int:task_id}
- Deletes the task having the requested task_id 
- Permission required: delete:task
- Returns: Id of the task that was deleted
- Sample: 
```
curl --request DELETE 'http://localhost:5000/tasks/3' \
--header 'Authorization: Bearer {your_access_token} \
--header 'Content-Type: application/json' \
--data-raw '{
	"status": "Complete"
}'
```
- Response:
```
{
  "deleted": 49,
  "success": true
}
```

GET /volunteers
- Gets all volunteers
- Permission required: get:volunteers
- Returns: A dictionary containing a list of all volunteers
- Sample: 
```
curl --request GET 'http://localhost:5000/volunteers' \
--header 'Authorization: Bearer {your_access_token}'
 ```
- Response:
```
{
  "success": true, 
  "volunteers": [
    {
      "address": "123 Maple St", 
      "city": "Anywhere", 
      "id": 3, 
      "name": "Jane Smith", 
      "phone_number": "404-123-4567", 
      "state": "GA", 
      "tasks": [], 
      "zip_code": "30303"
    }, 
    {
      "address": "111 Main St", 
      "city": "Seattle", 
      "id": 2, 
      "name": "Jim Bob Jones", 
      "phone_number": "123-456-7899", 
      "state": "WA", 
      "tasks": [
        {
          "date_needed": "2020-05-01", 
          "details": "Make 3 dozen ham and cheese sandwiches", 
          "id": 2, 
          "status": "Open", 
          "title": "Make Sandwiches", 
          "volunteer_id": 2, 
          "volunteer_name": "Jim Bob Jones"
        }
      ], 
      "zip_code": "93401"
    }, 
    {
      "address": "123 Maple St", 
      "city": "Somewhere", 
      "id": 1, 
      "name": "Joan Smith", 
      "phone_number": "404-123-4567", 
      "state": "GA", 
      "tasks": [
        {
          "date_needed": "2020-04-27", 
          "details": "Publix address: 123 Main St, OurTown", 
          "id": 1, 
          "status": "Open", 
          "title": "Pick up donations - Publix", 
          "volunteer_id": 1, 
          "volunteer_name": "Joan Smith"
        }
      ], 
      "zip_code": "9999-1234"
    }
  ]
}
```

GET /volunteers/{int:volunteer_id}
- Gets information about a particular volunteer
- Permission required: get:volunteer
- Returns: A dictionary containing a volunteer object whose id matches the requested volunteer_id
- Sample: `curl http://localhost:5000/volunteers/1`
```
curl --location --request GET 'http://localhost:5000/volunteers/1' \
--header 'Authorization: Bearer {your_access_token}'
```
- Response:
```
{
  "success": true,
  "volunteer": {
    "address": "123 Maple St",
    "city": "Somewhere",
    "id": 1,
    "name": "Joan Smith",
    "phone_number": "404-123-4567",
    "state": "GA",
    "tasks": [
      {
        "date_needed": "2020-04-27",
        "details": "Publix address: 123 Main St, OurTown",
        "id": 1,
        "status": "Open",
        "title": "Pick up donations - Publix",
        "volunteer_id": 1,
        "volunteer_name": "Joan Smith"
      }
    ],
    "zip_code": "9999-1234"
  }
```

POST /volunteers/create
- Creates a new volunteer with the given data
- Permission required: post:volunteer
- Required data: name, address, city, state, zip_code, phone_number
- Returns: The volunteer object that was created 
- Sample: 
```
curl --request POST 'http://localhost:5000/volunteers/create' \
--header 'Authorization: Bearer {your_access_token} \
--header 'Content-Type: application/json' \
--data-raw '{
	"name": "Kevin Bacon",
	"address": "123 Maple St",
	"city": "Anywhere",
	"state": "GA",
	"zip_code": "30303",
	"phone_number": "404-123-4567"
}'
```
- Response:
```
{
  "success": true,
  "volunteer": {
    "address": "123 Maple St",
    "city": "Anywhere",
    "id": 30,
    "name": "Kevin Bacon",
    "phone_number": "404-123-4567",
    "state": "GA",
    "tasks": [],
    "zip_code": "30303"
  }
}
```
 
PATCH /volunteers/{int:volunteer_id}
- Updates the volunteer having the requested volunteer_id with the given data.  
- Permission required: patch:volunteer
- Required data:  Only the fields to be updated should be included
- Returns: The updated volunteer object 
- Sample: 
```
curl --request PATCH 'http://localhost:5000/volunteerss/30' \
--header 'Authorization: Bearer {your_access_token} \
--header 'Content-Type: application/json' \
--data-raw '{
	"phone_number": "770-555-1212"
}'
```
- Response:
```
{
    "success": true,
    "volunteer": {
    "address": "123 Maple St",
    "city": "Anywhere",
    "id": 30,
    "name": "Kevin Bacon",
    "phone_number": "770-555-1212",
    "state": "GA",
    "tasks": [],
    "zip_code": "30303"
    }
}
```

DELETE /volunteers/{int:volunteer_id}
- Deletes the volunteer having the requested volunteer_id 
- Permission required: delete:volunteer
- Returns: Id of the volunteer that was deleted
- Sample: 
```
curl --request DELETE 'http://localhost:5000/tasks/3' \
--header 'Authorization: Bearer {your_access_token} 
```
- Response:
```
{
  "deleted": 3,
  "success": true
}
```

## Errors
Feed the Kids uses standard HTTP response codes to indicate the success or failture of an API request.
Errors are returned as JSON objects in the following format:
```
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```
Specific error codes are:
- 400 - Bad request.  The request was unacceptable, often due to a missing or invalid parameter
- 401 - Unauthorized.  You are not authorized to access the requested resource
- 404 - Not found.  The requested resource doesn't exist
- 405 - Method not allowed.  The requested method is not allowed for the endpoint
- 422 - Unprocessable.  The request could not be processed

## Authors
Dianne Gramling

## Acknowledgements
Thanks to the Udacity Full Stack Developer team!
