import unittest
import json
from app import create_app
from models import Volunteer

# https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}


class CapstoneTestCase(unittest.TestCase):
    """ This class represents the test cases for the Capstone app """
    # Task table must contain a row with id = 1.  This will be used to test
    # get_task and update_task
    # Task table must not contain a row with id = 99999. This will be used to
    # test for Not Found

    # Volunteer table must contain a row with id = 1.  This will be used to
    # test get_volunteer and update_volunteer
    # Volunteer table must not contain a row with id = 99999. This will be
    # used to test for Not Found

    # Set the following variable to an id that exists in the task table before
    # running.  It will be used to test delete_task
    delete_task_id = 36

    # Set the following variable to an id that exists in the Volunteer table
    # before running.  It will be used to test delete_volunteer
    delete_volunteer_id = 16

    def setUp(self):
        """ initialize the app """
        self.app = create_app()
        self.client = self.app.test_client

    # Task Tests ############################################################
    def test_get_all_tasks(self):
        res = self.client().get('/tasks')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['tasks'])

    def test_get_task_id_success(self):
        # Task table must contain a row id = 1
        task_id = 1
        res = self.client().get('/tasks/' + str(task_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['task'])

    def test_get_task_id_not_found(self):
        # Task table must not contain a row id = 99999
        task_id = 99999
        res = self.client().get('/tasks/' + str(task_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_update_task_success(self):
        # Task and Volunteer tables must each contain a row with id = 1
        task_id = 1
        vol_id = 1
        vol_name = Volunteer.query.get(vol_id).name

        res = self.client().patch('/tasks/' + str(task_id), json={
            'volunteer_id': vol_id
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['task'])
        self.assertEqual(data['task']['id'], task_id)
        self.assertEqual(data['task']['volunteer_id'], vol_id)
        self.assertEqual(data['task']['volunteer_name'], vol_name)

    def test_update_task_not_found(self):
        # Task table must not contain a row id = 99999
        task_id = 99999
        res = self.client().patch('/tasks/' + str(task_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_update_task_bad_request(self):
        # test contains no body
        task_id = 1
        res = self.client().patch('/tasks/' + str(task_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')

    def test_delete_task_success(self):
        res = self.client().delete('/tasks/' + str(self.delete_task_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['deleted'], self.delete_task_id)

    def test_delete_task_not_found(self):
        task_id = 99999
        res = self.client().delete('/tasks/' + str(task_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_create_task_success(self):
        date_needed = '2020-04-27'
        res = self.client().post('/tasks/create', json={
            'title': 'Pick up donations - Publix',
            'details': 'Publix address: 123 Main St, OurTown',
            'date_needed': date_needed
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['task'])
        self.assertEqual(data['task']['title'], 'Pick up donations - Publix')
        self.assertEqual(data['task']['details'],  'Publix address: 123 Main '
                                                   'St, OurTown')
        self.assertEqual(data['task']['date_needed'], date_needed)
        self.assertEqual(data['task']['status'], 'Open')
        self.assertEqual(data['task']['volunteer_id'],  None)
        self.assertEqual(data['task']['volunteer_name'],  '')

    def test_create_task_bad_request(self):
        # request omits a required field (date_needed)
        res = self.client().post('/tasks/create', json= {
            'title': 'Pick up donations from Kroger',
            'details': "Kroger's address: 456 Main St, OurTown, contact Jim"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')

# Volunteer Tests ############################################################
    def test_get_all_volunteers(self):
        res = self.client().get('/volunteers')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['volunteers'])

    def test_get_volunteer_id_success(self):
        # Volunteer table must contain a row with id = 1
        volunteer_id = '1'
        res = self.client().get('/volunteers/' + volunteer_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['volunteer'])

    def test_get_volunteer_id_not_found(self):
        # Volunteer table must not contain a row with id = 99999
        volunteer_id = '99999'
        res = self.client().get('/volunteers/' + volunteer_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_update_volunteer_success(self):
        # Volunteer table must contain a row with id = 1
        volunteer_id = '1'
        new_zip_code = '9999-1234'

        res = self.client().patch('/volunteers/' + volunteer_id, json={
            'zip_code': new_zip_code
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['volunteer'])
        self.assertEqual(data['volunteer']['zip_code'], new_zip_code)

    def test_update_volunteer_not_found(self):
        # Volunteer table must not contain a row with id = 99999
        volunteer_id = '99999'
        res = self.client().patch('/volunteers/' + volunteer_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_update_volunteer_bad_request(self):
        # this is a bad request because it does not contain a body
        volunteer_id = '1'
        res = self.client().patch('/volunteers/' + volunteer_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')

    def test_delete_volunteer_success(self):
        res = self.client().delete('/volunteers/' + str(self.delete_volunteer_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['deleted'], self.delete_volunteer_id)

    def test_delete_volunteer_not_found(self):
        # Volunteer table must not contain a row with id = 99999
        volunteer_id = '99999'
        res = self.client().delete('/volunteers/' + volunteer_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_create_volunteer_success(self):
        res = self.client().post('/volunteers/create', json={
            'name': 'Karen Jones',
            'address': '5555 Broadway',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '12345',
            'phone_number': '123-456-7890'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['volunteer'])
        self.assertEqual(data['volunteer']['name'], 'Karen Jones')
        self.assertEqual(data['volunteer']['address'], '5555 Broadway')
        self.assertEqual(data['volunteer']['city'], 'New York')
        self.assertEqual(data['volunteer']['state'], 'NY')
        self.assertEqual(data['volunteer']['zip_code'], '12345')
        self.assertEqual(data['volunteer']['phone_number'], '123-456-7890')
        self.assertEqual(data['volunteer']['tasks'], [])

    def test_create_volunteer_bad_request(self):
        # this is a bad request because it does not contain all of the
        # required fields
        res = self.client().post('/volunteers/create', json= {
            'name': 'Amy Adams'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')


if __name__ == '__main__':
    unittest.main()
