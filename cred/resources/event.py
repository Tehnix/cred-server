from flask_restful import Resource, reqparse
from cred import app, api
from cred.common import util


class Event(Resource):
    """Client transmitted events."""

    def post(self):
        rootParser = util.parser.copy()
        rootParser.add_argument('event', type=dict)
        rootArgs = rootParser.parse_args()
        eventParser = reqparse.RequestParser()
        eventParser.add_argument('location', type=str, location=('event',))
        eventParser.add_argument('action', type=str, location=('event',))
        eventParser.add_argument('value', location=('event',))
        eventArgs = eventParser.parse_args(req=rootArgs)
        return {
            'status': 'created',
            'event': {
                'action': eventArgs['action'],
                'value': eventArgs['value']
            }
        }, 201

