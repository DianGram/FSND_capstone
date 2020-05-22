# Feed the Kids Frontend

## Getting Started

This app is hosted on heroku, at https://for-the-kids.herokuapp.com/ or it can be run locally at http://localhost:5000

### Authentication 
Feed the Kids uses Auth0 for authentication.  The Auth0 JWT includes permissions for 2 different roles: Assistant and Director.
For the reviewer's convenience, there are logins already set up in Auth0 for each role:   
Assistant role - email is assistant@ftk.com and password is Assistant1   
Director role  - email is director@ftk.com and password is Director1   

###  Authorization
The Assistant role can add and update volunteers in the Volunteer table and they can update tasks in the Task table. 
To assign a volunteer to a task, the task is updated with a volunteer_id which is selected from a select field that
contains the names of all volunteers in alphabletical order.  The Assistant cannot add tasks nor can they delete
tasks or volunteers.

The Director role can add, update and delete volunteers and tasks.

The Public role can only view tasks with a status of Open.


