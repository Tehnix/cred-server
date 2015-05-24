import time
import random
import hashlib
import base64
from flask.ext.restful import reqparse, fields, marshal, request
from cred.database import db
from cred.exceptions import InvalidPermissions, APIKeyNotFound
from cred.common import util
from cred.models.apikey import APIKey as APIKeyModel


full_apikey_fields = {
    'id': fields.Integer,
    'apikey': fields.String,
    'permission': fields.String,
    'created': fields.DateTime(dt_format='rfc822'),
    'uri': fields.Url('apikeys_item', absolute=True),
}

simple_apikey_fields = {
    'id': fields.Integer,
    'uri': fields.Url('apikeys_item', absolute=True),
}


def generate_apikey():
    """Generate a unigue API key."""
    def _generate():
        apikey = base64.b64encode(
            hashlib.sha256((
                str(random.getrandbits(256)) +
                str(time.time())).encode('utf-8')
            ).digest(),
            random.choice(
                ['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD']
            ).encode('utf-8')
        ).decode('utf-8').rstrip('==')
        return apikey
    # Make sure the key doesn't exist
    apikey = _generate()
    while APIKeyModel.query.filter_by(apikey=apikey).first() is not None:
        apikey = _generate()
    return apikey


class APIKeys(util.AuthenticatedResource):
    """Methods going to the /apikeys route."""

    def post(self):
        """
        Create an API key with specified permissions.

        Available permissions are:
            read  - access to all GET requests (except API keys)
            write - access to all POST and GET requests (except API keys)
            admin - access to creating a API keys and everything else

        """
        self.require_admin_permission()
        parser = reqparse.RequestParser()
        parser.add_argument(
            'permission',
            type=str,
            required=True,
            location='json',
            help="A permission level needs to be specified")
        pargs = parser.parse_args()
        if pargs['permission'] not in ['read', 'write', 'admin']:
            raise InvalidPermissions()
        apikey = APIKeyModel(generate_apikey(), pargs['permission'])
        db.session.add(apikey)
        db.session.commit()
        # FIXME: Find out why the URI in marshalling causes problems
        # For now, manually create the URI
        apikeyMarshal = marshal(apikey, {
            'id': fields.Integer,
            'apikey': fields.String,
            'permission': fields.String,
            'created': fields.DateTime(dt_format='rfc822'),
            'uri': fields.Url('apikeys', absolute=True)
        })
        apikeyMarshal['uri'] = '{0}/{1}'.format(
            apikeyMarshal['uri'],
            apikey.id
        )
        return {
            'status': 201,
            'message': 'Created API Key',
            'apikey': apikeyMarshal
        }, 201

    def get(self):
        """
        Get a list of all API keys.

        Also accepts query parameters:
            full=<bool>
            before=<int>
            after=<int>
            limit=<int>
            offset=<int>
        which allows for a more fine-grained control.

        """
        self.require_admin_permission()
        apikeys = util.get_db_items(
            request,
            Model=APIKeyModel,
            default_fields=simple_apikey_fields,
            full_fields=full_apikey_fields
        )
        return {
            'status': 200,
            'message': 'OK',
            'apikeys': apikeys
        }, 200


class APIKeysItem(util.AuthenticatedResource):
    """Methods going to the /apikeys/<int:id> route."""

    def get(self, id):
        """Fetch information about a specific API key."""
        self.require_admin_permission()
        apikey = APIKeyModel.query.filter_by(id=id).first()
        if not apikey:
            raise APIKeyNotFound()
        return {
            'status': 200,
            'message': 'OK',
            'apikey': marshal(apikey, full_apikey_fields)
        }, 200
