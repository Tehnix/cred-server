from flask_restful import Resource, reqparse
from cred import api, db
from cred.common import util
from cred.resources.auth import client_from_session
from cred.models.event import Event as EventModel


def client_has_event(event_name, client):
    events = client.registered_events.all()
    for event in events:
        if event.name == event_name:
            return True
    return False


class Event(Resource):
    """General event actions."""

    def post(self):
        """Add a new event from a client."""
        # Set up the parser for the root of the object
        root_parser = util.parser.copy()
        root_parser.add_argument('event', type=dict)
        root_args = root_parser.parse_args()
        event_parser = reqparse.RequestParser()
        event_parser.add_argument('name', type=str, location=('event',))
        event_parser.add_argument('location', type=str, location=('event',))
        event_parser.add_argument('action', type=str, location=('event',))
        event_parser.add_argument('value', type=str, location=('event',))
        event_args = event_parser.parse_args(req=root_args)

        # Make sure the client actually has this event registered
        client = client_from_session(root_args['sessionKey'])
        if not client_has_event(event_args['name'], client):
            return {
                'status': 405,
                'message': 'Not Allowed'
            }, 405
        # Create the event in the database
        event = EventModel(
            client,
            event_args['name'],
            event_args['location'],
            event_args['action'],
            event_args['value']
        )
        db.session.add(event)
        db.session.commit()
        return {
            'status': 201,
            'message': 'Created',
            'event': {
                'id': event.id,
                'device': event.client.device,
                'name': event.name,
                'action': event.action,
                'value': event.value
            }
        }, 201

    def get(self):
        """Get the last event a client has submitted."""
        root_parser = util.parser.copy()
        root_args = root_parser.parse_args()
        client = client_from_session(root_args['sessionKey'])
        # Get the last event (it is sorted descending by id)
        event = client.events.first()
        return {
            'status': 200,
            'message': 'OK',
            'event': {
                'id': event.id,
                'device': event.client.device,
                'name': event.name,
                'action': event.action,
                'value': event.value
            }
        }, 200


class EventItem(Resource):
    """Actions on specific client events."""

    def get(self, event_id):
        """Get a specific event a client has submitted."""
        root_parser = util.parser.copy()
        root_args = root_parser.parse_args()
        client = client_from_session(root_args['sessionKey'])
        # Get the last event (it is sorted descending by id)
        event = EventModel.query.filter_by(id=event_id).first()
        return {
            'status': 200,
            'message': 'OK',
            'event': {
                'id': event.id,
                'device': event.client.device,
                'name': event.name,
                'action': event.action,
                'value': event.value
            }
        }, 200

