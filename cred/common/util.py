from functools import wraps
from datetime import datetime
from flask.ext.restful import Resource, reqparse, abort
from cred import db
from cred.models.client import Client


parser = reqparse.RequestParser()
parser.add_argument(
    'sessionKey',
    type=str,
    location='cookies'
)


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
        self.get_client()

    def get_client(self):
        """
        Get the client from the session key in the cookies, and update the time
        that the client was last active.

        """
        pargs = parser.parse_args()
        session_key = pargs['sessionKey']
        client = Client.query.filter_by(session=session_key).first()
        if not client:
            abort(401)
        client.last_active = datetime.utcnow()
        self.client = client
        self.authenticated = True
