import unittest
import os
import json
from app import create_app, db


class UserTests(unittest.TestCase):
    """
    User Test cases
    """

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.user = {
            'name': 'John',
            'email': 'John@email.com',
            'password': 'passw0rd!'
        }

        with self.app.app_context():
            db.create_all()

    def test_success_user_creation(self):
        """
             test user creation
             """
        response_received = self.client.post('/api/v1/users/',
                                             headers={'Content-Type': 'application/json'},
                                             data=json.dumps(self.user))
        json_data = json.loads(response_received.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertTrue(response_received.status_code, 201)

    def test_user_creation_with_existing_email(self):
        """ test user creation with already existing email"""
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('error'))

    def test_user_login(self):
        """ User Login Tests """
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 200)

    def teardown(self):
        """
            Tear down db
            """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
