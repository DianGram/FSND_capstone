# Feed the Kids

## Udacity Full Stack NanoDegree Capstone Project

### Overview
For my Capstone project, I am implementing a simplified app for a non-profit called Feed the Kids.  
It is to be used by the public to view opportunities to volunteer and by employees of the company to
manage tasks and volunteers.
There are two tables: Tasks and Volunteers, and two roles:  Assistant and Director. Auth0 is used to authenticate users.
* The Assistant Role:
    *  Can view, create, and update Volunteers
    *  Can view and update Tasks

* The Director Role:
    * Can view, create, update and delete Volunteers
    * Can view, create, update and delete Tasks

* The public:
    * Can view open tasks

## About the Tech Stack
The tech stack will include:

* **SQLAlchemy** 
* **PostgreSQL** 
* **Python3** 
* **Flask** 
* **Flask-Migrate** 
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 4](https://getbootstrap.com/docs/4.5/getting-started/introduction/) for our website's frontend

### Backend
[View the ./backend README.md for more details.](./backend/README.md)

### Frontend
[View the ./frontend README.md for more details.](./frontend/README.md)
