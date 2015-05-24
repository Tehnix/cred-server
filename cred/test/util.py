import os
import tempfile
import json
from functools import wraps
import flask.ext.testing
import flask.ext.sqlalchemy
import cred.config
import cred.database
from cred.app import app, api
from cred.routes import create_api_resources


# Constants used throughout the test suites
DEVICE = 'Thermostat'
LOCATION = 'Living Room'
EVENTS = ['Temperature']
SUBSCRIBE = {
    'Light': {'location': 'Living Room'},
    'Alarm': {}
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
cred.database.db = flask.ext.sqlalchemy.SQLAlchemy(app)
create_api_resources(api)
cred.config.loaded_configuration = cred.config.default_config


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


class BaseTestCase(flask.ext.testing.TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        return app

    def setUp(self):
        """Create a SQLite database for quick testing."""
        cred.database.init_db(cred.database.db)
        self.session_key = None

    def tearDown(self):
        """Close the database file and unlink it."""
        cred.database.db.session.remove()
        cred.database.db.drop_all()

    def authenticate_with_server(self, permission, alternate_device=None):
        """Authenticate with the server."""
        from cred.models.apikey import APIKey as APIKeyModel
        from cred.resources.apikeys import generate_apikey
        device = DEVICE
        if alternate_device is not None:
            device = alternate_device
        apikey = APIKeyModel(generate_apikey(), permission)
        cred.database.db.session.add(apikey)
        cred.database.db.session.commit()
        req = json.dumps({
            'apikey': apikey.apikey,
            'device': device,
            'location': LOCATION,
            'subscribe': SUBSCRIBE
        })
        response = self.client.post(
            '/auth',
            data=req,
            content_type='application/json'
        )
        resp = json.loads(response.data.decode('utf-8'))
        self.session_key = resp['sessionKey']
        self.id = resp['id']
        return response
