import os
import tempfile
import json
from functools import wraps
from flask.ext.testing import TestCase
from flask.ext.sqlalchemy import SQLAlchemy
import cred
from cred.models.apikey import APIKey as APIKeyModel
from cred.resources.apikeys import generate_apikey


# Constants used throughout the test suites
DEVICE = 'Thermostat'
LOCATION = 'Living Room'
EVENTS = ['Temperature']
SUBSCRIBE = {
    'Light': {'location': 'Living Room'},
    'Alarm': {}
}


def assertEqual(test_object, assertables):
    """Convenience method for asserting multiple items."""
    for value, expected_value in assertables.items():
        test_object.assertEqual(value, expected_value)


def authenticate(permission, alt_dev=None):
    """Decorator for authenticating a client with permissions."""
    def authenticate_decorator(fun):
        @wraps(fun)
        def wrapped(self, *args, **kwargs):
            self.authenticate_with_server(permission, alternate_device=alt_dev)
            fun(self, *args, **kwargs)
        return wrapped
    return authenticate_decorator


class BaseTestCase(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        return cred.app

    def setUp(self):
        """Create a SQLite database for quick testing."""
        self.client = cred.app.test_client()
        cred.initDB()
        self.session_key = None

    def tearDown(self):
        """Close the database file and unlink it."""
        cred.db.session.remove()
        cred.db.drop_all()

    def authenticate_with_server(self, permission, alternate_device=None):
        """Authenticate with the server."""
        device = DEVICE
        if alternate_device is not None:
            device = alternate_device
        apikey = APIKeyModel(generate_apikey(), permission)
        cred.db.session.add(apikey)
        cred.db.session.commit()
        req = json.dumps({
            'apiKey': apikey.apikey,
            'device': device,
            'location': LOCATION,
            'subscribe': SUBSCRIBE
        })
        response = self.client.post(
            '/auth',
            data=req,
            content_type='application/json')
        resp = json.loads(response.data.decode('utf-8'))
        self.session_key = resp['sessionKey']
        self.client_id = resp['id']
        return response
