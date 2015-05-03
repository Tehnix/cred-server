import hashlib
import random
import time
import json
from flask.ext.restful import Resource, reqparse
from cred import db
from cred.models.client import Client
from cred.models.subscribe import Subscribe


def create_client_session_key(api_key):
    """Create a unique session key for the client."""
    session_key = hashlib.sha256()
    session_key.update(str(random.getrandbits(255)).encode('utf-8'))
    session_key.update(str(time.time()).encode('utf-8'))
    session_key.update(api_key.encode('utf-8'))
    return session_key.hexdigest()


def subscribe_to_events(client, subscribe):
    for device in subscribe:
        location = None
        if 'location' in subscribe[device]:
            location = subscribe[device]['location']
        sub = Subscribe(client, device, location)
        db.session.add(sub)


class Auth(Resource):
    """Authenticate the client, and schedule it if implemented."""

    def post(self):
        # Set up the parser for the root of the object
        parser = reqparse.RequestParser()
        parser.add_argument(
            'apiKey',
            type=str,
            required=True,
            location='json',
            help="An API key is required!")
        parser.add_argument('device', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('events', type=str, action='append')
        parser.add_argument('subscribe', type=dict)
        pargs = parser.parse_args()

        session_key = create_client_session_key(pargs['apiKey'])
        # Register the client information to the session key
        client = Client(pargs['device'], pargs['location'], session_key)
        db.session.add(client)
        # Subscribe the client to the requested events
        subscribe_to_events(client, pargs['subscribe'])
        db.session.commit()

        subscribes = {}
        for item in client.subscribes.all():
            subscribes[item.event] = {'location': item.location}

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
            'subscribe': subscribes
        }, 201, {'Set-Cookie': 'sessionKey=' + session_key}
