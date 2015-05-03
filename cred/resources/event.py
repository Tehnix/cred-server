from datetime import datetime
from flask.ext.restful import reqparse
from cred import db
from cred.common import util
from cred.models.event import Event as EventModel


class Event(util.AuthenticatedResource):
    """General event actions."""

    def post(self):
        """Create a new event."""
        # Set up the parser for the root of the object
        parser = reqparse.RequestParser()
        parser.add_argument('event', type=dict)
        pargs = parser.parse_args()
        event_args = util.add_nested_arguments(pargs, 'event', {
            'name': str,
            'location': str,
            'action': str,
            'value': str
        })

        # Create the event in the database
        event = EventModel(
            self.client,
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
        """Get all new events since the client last pulled for them."""
        event = self.client.events.order_by(EventModel.id.desc()).first()
        self.client.last_pull = datetime.utcnow()
        if not event:
            return {
                'status': 200,
                'message': 'OK',
                'newEvents': False,
                'events': {}
            }, 200
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


class EventAll(util.AuthenticatedResource):
    """Actions on multiple events."""

    def get(self):
        pass


class EventItem(util.AuthenticatedResource):
    """Actions on specific client events."""

    def get(self, event_id):
        """Fetch a specific event a client has requested."""
        # Get the last event (it is sorted descending by id)
        event = EventModel.query.filter_by(id=event_id).first()
        if not event:
            return {
                'status': 404,
                'message': 'Not Found'
            }, 404
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
