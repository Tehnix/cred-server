import hashlib
import random
import time
import json
from flask.ext.restful import Resource, reqparse
import cred.config
from cred.database import db
from cred.exceptions import InvalidAPIKey
from cred.models.apikey import APIKey as APIKeyModel
from cred.models.client import Client as ClientModel
from cred.models.subscribe import Subscribe as SubscribeModel


def create_client_session_key(apikey):
    """Create a unique session key for the client."""
    session_key = hashlib.sha256()
    session_key.update(str(random.getrandbits(255)).encode('utf-8'))
    session_key.update(str(time.time()).encode('utf-8'))
    session_key.update(apikey.encode('utf-8'))
    return session_key.hexdigest()


def subscribe_to_events(client, subscribe):
    for device in subscribe:
        location = None
        if 'location' in subscribe[device]:
            location = subscribe[device]['location']
        sub = SubscribeModel(client, device, location)
        db.session.add(sub)


class Auth(Resource):
    """Methods going to the /auth route."""

    def post(self):
        """Authenticate the client, and schedule it if implemented."""
        parser = reqparse.RequestParser()
        parser.add_argument('apikey', type=str)
        parser.add_argument('device', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('subscribe', type=dict)
        pargs = parser.parse_args()

        apikey = APIKeyModel.query.filter_by(apikey=pargs['apikey']).first()
        if pargs['apikey'] is None or not apikey:
            apikeys = APIKeyModel.query.all()
            raise InvalidAPIKey()
        session_key = create_client_session_key(pargs['apikey'])
        # Register the client information to the session key
        client = ClientModel(
            pargs['device'],
            pargs['location'],
            session_key,
            apikey
        )
        db.session.add(client)
        # Subscribe the client to the requested events
        if pargs['subscribe']:
            subscribe_to_events(client, pargs['subscribe'])
        db.session.commit()

        subscribes = {}
        for item in client.subscribes.all():
            subscribes[item.event] = {'location': item.location}
        if cred.config.loaded_configuration['scheduler']:
            # Very simple scheduler, that assigns a random timeslot
            scheduled = {
                'assigned': True,
                'slot': random.randrange(1,31),
                'period': cred.config.loaded_configuration['schedulerPeriod']
            }
        else:
            scheduled = {
                'assigned': False,
                'slot': None,
                'period': None
            }
        # FIXME: Set cookie in a proper way!
        return {
            'status': 201,
            'message': 'Authenticated',
            'id': client.id,
            'sessionKey': session_key,
            'scheduled': scheduled,
            'PINGTimeout': cred.config.loaded_configuration['pingtimeout']
        }, 201, {'Set-Cookie': 'sessionKey=' + session_key}
