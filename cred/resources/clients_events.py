from flask import request
from flask.ext.restful import reqparse, fields, marshal
from cred.exceptions import ClientNotFound
from cred.common import util
from cred.models.client import Client as ClientModel
from cred.models.event import Event as EventModel
from cred.resources.events import get_subscribed_events, simple_event_fields, full_event_fields


class ClientsEvents(util.AuthenticatedResource):
    """Methods going to the /clients/<int:id>/events route."""

    def get(self, id):
        """
        Get a list of all events the client has created.

        Also accepts query parameters:
            full=<bool>
            before=<int>
            after=<int>
            limit=<int>
            offset=<int>
        which allows for a more fine-grained control.

        """
        self.require_read_permission()
        client = ClientModel.query.filter_by(id=id).first()
        if not client:
            raise ClientNotFound()
        events = util.get_db_items(
            request,
            Model=EventModel,
            default_fields=simple_event_fields,
            full_fields=full_event_fields,
            base_query=client.events
        )
        if not events:
            return {
                'status': 200,
                'message': 'OK',
                'events': []
            }, 200
        return {
            'status': 200,
            'message': 'OK',
            'events': events
        }, 200


class ClientsSubscribedEvents(util.AuthenticatedResource):
    """Methods going to the /clients/<int:id>/subscribedevents route."""

    def get(self, id):
        """
        Get a list of all events the client has subscribed to.

        Also accepts query parameters:
            full=<bool>
            before=<int>
            after=<int>
            limit=<int>
            offset=<int>
        which allows for a more fine-grained control.

        """
        self.require_read_permission()
        client = ClientModel.query.filter_by(id=id).first()
        if not client:
            raise ClientNotFound()
        events = get_subscribed_events(
            request,
            client
        )
        if not events:
            return {
                'status': 200,
                'message': 'OK',
                'events': []
            }, 200
        return {
            'status': 200,
            'message': 'OK',
            'events': events
        }, 200
