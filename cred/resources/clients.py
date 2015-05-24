import datetime
from flask import request
from flask.ext.restful import reqparse, fields, marshal
import cred.config
from cred.exceptions import ClientNotFound
from cred.common import util
from cred.models.client import Client as ClientModel


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


class Clients(util.AuthenticatedResource):
    """Methods going to the /clients route."""

    def get(self):
        """
        Get a list of all active clients, based on pingtimeout configuration.

        Also accepts query parameters:
            full=<bool>
            before=<int>
            after=<int>
            limit=<int>
            offset=<int>
        which allows for a more fine-grained control.

        """
        self.require_read_permission()
        clients = util.get_db_items(
            request,
            Model=ClientModel,
            default_fields=simple_client_fields,
            full_fields=full_client_fields,
            base_query=ClientModel.query.filter(
                ClientModel.last_active > (datetime.datetime.utcnow() - datetime.timedelta(seconds=cred.config.loaded_configuration['pingtimeout']))
            )
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
        self.require_read_permission()
        client = self.client
        return {
            'status': 200,
            'message': 'OK',
            'client': marshal(client, full_client_fields)
        }, 200


class ClientsItem(util.AuthenticatedResource):
    """Methods going to the /clients/<int:id> route."""

    def get(self, id):
        """Fetch information about a specific client."""
        self.require_read_permission()
        client = ClientModel.query.filter_by(id=id).first()
        if not client:
            raise ClientNotFound()
        return {
            'status': 200,
            'message': 'OK',
            'client': marshal(client, full_client_fields)
        }, 200
