from functools import wraps
from datetime import datetime
from flask.ext.restful import Resource, reqparse, abort, marshal
from cred.database import db
from cred.exceptions import NotAuthenticated, InsufficientPermissions
from cred.models.client import Client


parser = reqparse.RequestParser()
parser.add_argument(
    'sessionKey',
    type=str,
    location=['cookies', 'json']
)


def get_db_items(request, Model=None, default_fields=None, full_fields=None, base_query=None):
    """Generalized database retrieval with support for parameters."""
    # Either use an already initated query, or start a standard query
    if base_query is not None:
        query = base_query
    else:
        query = Model.query
    query = query.order_by(db.desc(Model.id))
    # Add filters to the query, based on the request
    if request.args.get('before', False):
        query = query.filter(
            Model.id < request.args.get('before', 0)
        )
    if request.args.get('after', False):
        query = query.filter(
            Model.id > request.args.get('after', 0)
        )
    if request.args.get('limit', False):
        query = query.limit(request.args.get('limit', 0))
    if request.args.get('offset', False):
        query = query.offset(request.args.get('offset', 0))
    # Retrive the rows from the database
    query = query.all()
    # Finally, marshal it before returning the result
    if request.args.get('full', False) and full_fields is not None:
        return marshal(query, full_fields)
    else:
        return marshal(query, default_fields)


def add_nested_arguments(top_pargs, location, args):
    """Quickly add arguments multiple nested arguments to a parser."""
    parser = reqparse.RequestParser()
    for name, arg_type in args.items():
        parser.add_argument(
            name,
            type=arg_type,
            location=location
        )
    return parser.parse_args(req=top_pargs)



class AuthenticatedResource(Resource):
    """Base class for a resource that requires authentication."""

    def __init__(self):
        """Automatically try to authenticate the client."""
        super(AuthenticatedResource, self).__init__()
        self.client = None
        self.authenticated = False
        self.authenticate()

    def require_admin_permission(self):
        if self.client.apikey.permission != 'admin':
            raise InsufficientPermissions()

    def require_write_permission(self):
        if self.client.apikey.permission not in ['admin', 'write']:
            raise InsufficientPermissions()

    def require_read_permission(self):
        if self.client.apikey.permission not in ['admin', 'write', 'read']:
            raise InsufficientPermissions()

    def authenticate(self):
        """
        Get the client from the session key in the cookies, and update the time
        that the client was last active.

        """
        pargs = parser.parse_args()
        session_key = pargs['sessionKey']
        client = Client.query.filter_by(session=session_key).first()
        if not client:
            raise NotAuthenticated()
        client.last_active = datetime.utcnow()
        self.client = client
        self.authenticated = True
