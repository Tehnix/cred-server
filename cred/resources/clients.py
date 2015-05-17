from datetime import datetime
from collections import OrderedDict
from flask import request
from flask.ext.restful import reqparse, fields, marshal
from cred import db
from cred.common import util
from cred.models.client import Client as ClientModel
from cred.resources.events import get_events, get_subscribed_events


full_client_fields = {
    'id': fields.Integer,
    'device': fields.String,
    'location': fields.String,
    'uri': fields.Url('clients_item', absolute=True),
}

simple_client_fields = {
    'id': fields.Integer,
    'uri': fields.Url('clients_item', absolute=True),
}


def get_clients(base_query=None, full=False, after=None, before=None, limit=None, offset=None):
    if base_query is not None:
        clients = base_query
    else:
        clients = ClientModel.query
    # Add filters to the clients, based on the request
    if before is not None:
        clients = clients.filter(
            ClientModel.id < before
        )
    if after is not None:
        clients = clients.filter(
            ClientModel.id > after
        )
    if limit is not None:
        clients = clients.limit(limit)
    if offset is not None:
        clients = clients.offset(offset)
    clients = clients.all()
    if full:
        return marshal(clients, full_client_fields)
    else:
        return marshal(clients, simple_client_fields)


class Clients(util.AuthenticatedResource):
    """Methods going to the /clients route."""

    def get(self):
        """
        Get a list of all active clients.

        Also accepts query parameters:
            full=<bool>
            before=<int>
            after=<int>
            limit=<int>
            offset=<int>
        which allows for a more fine-grained control.

        """
        clients = get_clients(
            full=request.args.get('full', False),
            before=request.args.get('before', None),
            after=request.args.get('after', None),
            limit=request.args.get('limit', None),
            offset=request.args.get('offset', None)
        )
        return {
            'status': 200,
            'message': 'OK',
            'clients': clients
        }, 200


class ClientsMe(util.AuthenticatedResource):
    """Methods going to the /clients/me route."""

    def get(self):
        """Fetch information about the client itself."""
        client = self.client
        if not client:
            return {
                'status': 404,
                'message': 'Client Not Found!'
            }, 404
        return {
            'status': 200,
            'message': 'OK',
            'client': marshal(client, full_client_fields)
        }, 200


class ClientsItem(util.AuthenticatedResource):
    """Methods going to the /clients/<int:id> route."""

    def get(self, id):
        """Fetch information about a specific client."""
        client = ClientModel.query.filter_by(id=id).first()
        if not client:
            return {
                'status': 404,
                'message': 'Client Not Found!'
            }, 404
        return {
            'status': 200,
            'message': 'OK',
            'client': marshal(client, full_client_fields)
        }, 200
