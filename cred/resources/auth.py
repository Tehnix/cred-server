import hashlib
import random
import time
from flask_restful import Resource, reqparse
from cred import db
from cred.models.client import Client
from cred.models.registered_event import RegisteredEvent
from cred.models.subscribe import Subscribe


def create_client_session_key(api_key):
    """Create a unique session key for the client."""
    session_key = hashlib.sha256()
    session_key.update(str(random.getrandbits(255)).encode('utf-8'))
    session_key.update(str(time.time()).encode('utf-8'))
    session_key.update(api_key.encode('utf-8'))
    return session_key.hexdigest()

def client_from_session(session_key):
    return Client.query.filter_by(session=session_key).first()


class Auth(Resource):
    """Authenticate the client, and schedule it if implemented."""

    def post(self):
        # Set up the parser for the root of the object
        root_parser = reqparse.RequestParser()
        root_parser.add_argument(
            'apiKey',
            type=str,
            required=True,
            location='json',
            help="An API key is required!")
        root_parser.add_argument('device', type=str)
        root_parser.add_argument('location', type=str)
        root_parser.add_argument('events', type=str, action='append')
        root_parser.add_argument('subscribe', type=dict)
        root_args = root_parser.parse_args()

        session_key = create_client_session_key(root_args['apiKey'])
        # Create a client database object from our model
        c = Client(root_args['device'], root_args['location'], session_key)
        db.session.add(c)
        # Add events to the database, linked to the client
        for event in root_args['events']:
            e = RegisteredEvent(c, event)
            db.session.add(e)
        # Construct a list of subscribed events and also add them to the
        # database
        subscribed = []
        subscribe = root_args['subscribe']
        for device in subscribe:
            if 'location' in subscribe[device]:
                location = subscribe[device]['location']
            else:
                location = None
            s = Subscribe(c, device, location)
            subscribed.append(device)
            db.session.add(s)

        # Write the data and return a response
        db.session.commit()
        # FIXME: Set cookie in a proper way!
        return {
            'status': 201,
            'message': 'Created',
            'sessionKey': session_key,
            'scheduled': {
                'assigned': False,
                'slot': None
            },
            'PINGTimeout': 240,
            'subscribe': subscribed
        }, 201, {'Set-Cookie': 'sessionKey=' + session_key}

