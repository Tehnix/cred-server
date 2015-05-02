from cred import api
from cred.resources.auth import Auth
from cred.resources.event import Event, EventItem
from cred.resources.ping import Ping


api.add_resource(Auth, '/auth')
api.add_resource(Event, '/event')
api.add_resource(EventItem, '/event/<int:event_id>')
api.add_resource(Ping, '/ping')

