from datetime import datetime
from collections import OrderedDict
from flask.ext.restful import reqparse
from cred import db
from cred.common import util
from cred.models.event import Event as EventModel


def get_new_events(client, full_information=False):
    subscribes = client.subscribes
    events = []
    for subscribtion in subscribes:
        if subscribtion.location is None:
            subscribed_events = EventModel.query.filter(
                EventModel.time >= client.last_pull
            ).filter(
                EventModel.name == subscribtion.event
            ).all()
        else:
            subscribed_events = EventModel.query.filter(
                EventModel.time >= client.last_pull
            ).filter(
                EventModel.location == subscribtion.location
            ).filter(
                EventModel.name == subscribtion.event
            ).all()
        for event in subscribed_events:
            if full_information:
                events.append({
                    'id': event.id,
                    'device': event.client.device,
                    'name': event.name,
                    'action': event.action,
                    'value': event.value,
                    'time': event.time.isoformat()
                })
            else:
                events.append({'id': event.id})
    return sorted(events, key=lambda item: item['id'])


class Events(util.AuthenticatedResource):
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
                'value': event.value,
                'time': event.time.isoformat()
            }
        }, 201

    def get(self):
        """Get all IDs for new events since the client last pulled for them."""
        # Gather the IDs for all events the client has subscribed to
        events = get_new_events(self.client)
        # Update the time the client last pulled event information
        self.client.last_pull = datetime.utcnow()
        db.session.commit()
        if not events:
            return {
                'status': 200,
                'message': 'OK',
                'newEvents': False,
                'events': []
            }, 200
        return {
            'status': 200,
            'message': 'OK',
            'newEvents': True,
            'events': events
        }, 200


class EventsFull(util.AuthenticatedResource):
    """Actions on multiple events."""

    def get(self):
        """Get data for new events since the client last pulled for them."""
        # Gather the IDs for all events the client has subscribed to
        events = get_new_events(self.client, full_information=True)
        # Update the time the client last pulled event information
        self.client.last_pull = datetime.utcnow()
        db.session.commit()
        if not events:
            return {
                'status': 200,
                'message': 'OK',
                'newEvents': False,
                'events': []
            }, 200
        return {
            'status': 200,
            'message': 'OK',
            'newEvents': True,
            'events': events
        }, 200


class EventsItem(util.AuthenticatedResource):
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
