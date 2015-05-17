from datetime import datetime
from collections import OrderedDict
from flask import request
from flask.ext.restful import reqparse, fields, marshal
from cred import db
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
    'uri': fields.Url('events_item', absolute=True),
}

simple_event_fields = {
    'id': fields.Integer,
    'uri': fields.Url('events_item', absolute=True),
}


def get_subscribed_events(client, full=False, after=None, before=None, limit=None, offset=None):
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
        subscribed_events = get_events(
            base_query=subscribed_events,
            full=full,
            after=after,
            before=before
        )
        events += subscribed_events
    # Sort the events on ID before returning them
    return sorted(events, key=lambda item: item['id'])


def get_events(base_query=None, full=False, after=None, before=None, limit=None, offset=None):
    if base_query is not None:
        events = base_query
    else:
        events = EventModel.query
    # Add filters to the events, based on the request
    if before is not None:
        events = events.filter(
            EventModel.id < before
        )
    if after is not None:
        events = events.filter(
            EventModel.id > after
        )
    if limit is not None:
        events = events.limit(limit)
    if offset is not None:
        events = events.offset(offset)
    events = events.all()
    if full:
        return marshal(events, full_event_fields)
    else:
        return marshal(events, simple_event_fields)


class Events(util.AuthenticatedResource):
    """Methods going to the /events route."""

    def post(self):
        """Create a new event and return the id and uri of the event."""
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
        return {
            'status': 201,
            'message': 'Created Event',
            'event': marshal(event, simple_event_fields)
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
        events = get_events(
            full=request.args.get('full', False),
            before=request.args.get('before', None),
            after=request.args.get('after', None),
            limit=request.args.get('limit', None),
            offset=request.args.get('offset', None)
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
        # Get the last event (it is sorted descending by id)
        event = EventModel.query.filter_by(id=id).first()
        if not event:
            return {
                'status': 404,
                'message': 'Event Not Found!'
            }, 404
        return {
            'status': 200,
            'message': 'OK',
            'event': marshal(event, full_event_fields)
        }, 200
