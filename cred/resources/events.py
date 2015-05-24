from flask import request, url_for
from flask.ext.restful import reqparse, fields, marshal
from cred.database import db
from cred.exceptions import EventNotFound
from cred.common import util
from cred.models.event import Event as EventModel


full_event_fields = {
    'id': fields.Integer,
    'device': fields.String(attribute='client.device'),
    'name': fields.String,
    'location': fields.String,
    'action': fields.String,
    'value': fields.String,
    'time': fields.DateTime(dt_format='rfc822'),
    'uri': fields.Url('events_item', absolute=True)
}

simple_event_fields = {
    'id': fields.Integer,
    'uri': fields.Url('events_item', absolute=True)
}


def get_subscribed_events(request, client):
    # Get the events that the client subscribes to
    subscribes = client.subscribes
    # Put all events into a list of events
    events = []
    for subscribtion in subscribes:
        # Get all events that match the subscribtion event name
        subscribed_events = EventModel.query.filter(
            EventModel.name == subscribtion.event
        )
        # Add location to filter, if specified
        if subscribtion.location is not None:
            subscribed_events = subscribed_events.filter(
                EventModel.location == subscribtion.location
            )
        # Add filters to the events, based on the request
        subscribed_events = util.get_db_items(
            request,
            Model=EventModel,
            default_fields=simple_event_fields,
            full_fields=full_event_fields,
            base_query=subscribed_events,
        )
        events += subscribed_events
    # Sort the events on ID before returning them
    return sorted(events, key=lambda item: item['id'], reverse=True)


class Events(util.AuthenticatedResource):
    """Methods going to the /events route."""

    def post(self):
        """Create a new event and return the id and uri of the event."""
        self.require_write_permission()
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
        # Save the event in the database
        db.session.add(event)
        db.session.commit()
        # Finally, convert the event object into our format by marshalling it,
        # and returning the JSON object
        # FIXME: Find out why the URI in marshalling causes problems
        # For now, manually create the URI
        eventMarshal = marshal(event, {
            'id': fields.Integer,
            'uri': fields.Url('events', absolute=True)
        })
        eventMarshal['uri'] = '{0}/{1}'.format(
            eventMarshal['uri'],
            event.id
        )
        return {
            'status': 201,
            'message': 'Created Event',
            'event': eventMarshal
        }, 201

    def get(self):
        """
        Get a list of all events.

        Also accepts query parameters:
            full=<bool>
            before=<int>
            after=<int>
            limit=<int>
            offset=<int>
        which allows for a more fine-grained control.

        """
        self.require_read_permission()
        events = util.get_db_items(
            request,
            Model=EventModel,
            default_fields=simple_event_fields,
            full_fields=full_event_fields
        )
        if not events:
            events = []
        return {
            'status': 200,
            'message': 'OK',
            'events': events
        }, 200


class EventsItem(util.AuthenticatedResource):
    """Methods going to the /events/<int:id> route."""

    def get(self, id):
        """Fetch a specific event."""
        self.require_read_permission()
        # Get the last event (it is sorted descending by id)
        event = EventModel.query.filter_by(id=id).first()
        if not event:
            raise EventNotFound()
        return {
            'status': 200,
            'message': 'OK',
            'event': marshal(event, full_event_fields)
        }, 200
