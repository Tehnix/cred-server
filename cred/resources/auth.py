from flask_restful import Resource, reqparse
from cred import db
from cred.common import util
from cred.models.client import Client


class Auth(Resource):
    """Authenticate the client, and schedule it if implemented."""

    def post(self):
        rootParser = util.parser.copy()
        rootParser.add_argument('device', type=str)
        rootParser.add_argument('location', type=str)
        rootParser.add_argument('events', type=list)
        rootParser.add_argument('subscribes', type=dict)
        rootArgs = rootParser.parse_args()
        subParser = reqparse.RequestParser()
        subParser.add_argument('location', type=str, location=('subscribes',))
        subArgs = subParser.parse_args(req=rootArgs)
        client = Client(
            rootArgs['device'],
            rootArgs['location'],
            rootArgs['apiKey'])
        db.session.add(client)
        db.session.commit()
        
        return {
            'status': 'created',
            'scheduled': {
                'assigned': False,
                'slot': None
            },
            'PINGTimeout': 240
        }, 201

