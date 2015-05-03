from cred import api
from cred.resources.auth import Auth
from cred.resources.event import Event, EventAll, EventItem


api.add_resource(Auth, '/auth')
api.add_resource(Event, '/events')
api.add_resource(EventAll, '/events/all')
api.add_resource(EventItem, '/events/<int:event_id>')
