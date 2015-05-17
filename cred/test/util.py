import os
import tempfile
import unittest
import json
from functools import wraps
import cred


# Constants used throughout the test suites
API_KEY = 'uJidciTE1fuJXf37gs8MgPskMjYLxe'
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


def authenticate(fun):
    """Decorator for authenticating a client."""
    @wraps(fun)
    def wrapped(self, *args, **kwargs):
        self.authenticate_with_server()
        fun(self, *args, **kwargs)
    return wrapped


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Create a SQLite database for quick testing."""
        self.db_file_descriptor, self.dbfile = tempfile.mkstemp()
        cred.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        cred.app.config['SQLALCHEMY_DATABASE_URI'] += self.dbfile
        cred.app.config['TESTING'] = True
        self.app = cred.app.test_client()
        self.session_key = None
        cred.initDB()

    def tearDown(self):
        """Close the database file and unlink it."""
        os.close(self.db_file_descriptor)
        os.unlink(self.dbfile)

    def authenticate_with_server(self, alternate_device=None):
        """Authenticate with the server."""
        device = DEVICE
        if alternate_device is not None:
            device = alternate_device
        req = json.dumps({
            'apiKey': API_KEY,
            'device': device,
            'location': LOCATION,
            'events': EVENTS,
            'subscribe': SUBSCRIBE
        })
        response = self.app.post(
            '/auth',
            data=req,
            content_type='application/json')
        resp = json.loads(response.data.decode('utf-8'))
        self.session_key = resp['sessionKey']
        self.client_id = resp['id']
        return response
