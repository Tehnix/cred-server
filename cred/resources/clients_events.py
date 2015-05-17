from datetime import datetime
from collections import OrderedDict
from flask import request
from flask.ext.restful import reqparse, fields, marshal
from cred import db
from cred.common import util
from cred.models.client import Client as ClientModel
from cred.resources.events import get_events, get_subscribed_events


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
        client = ClientModel.query.filter_by(id=id).first()
        if not client:
            return {
                'status': 404,
                'message': 'Client Not Found!'
            }, 404
        events = get_events(
            base_query=client.events,
            full=request.args.get('full', False),
            before=request.args.get('before', None),
            after=request.args.get('after', None),
            limit=request.args.get('limit', None),
            offset=request.args.get('offset', None)
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
        client = ClientModel.query.filter_by(id=id).first()
        if not client:
            return {
                'status': 404,
                'message': 'Client Not Found!'
            }, 404
        events = get_subscribed_events(
            client,
            full=request.args.get('full', False),
            before=request.args.get('before', None),
            after=request.args.get('after', None),
            limit=request.args.get('limit', None),
            offset=request.args.get('offset', None)
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
