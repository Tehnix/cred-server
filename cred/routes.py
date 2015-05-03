from cred import api
from cred.resources.auth import Auth
from cred.resources.event import Events, EventsFull, EventsItem


api.add_resource(Auth, '/auth')
api.add_resource(Events, '/events')
api.add_resource(EventsFull, '/events/full')
api.add_resource(EventsItem, '/events/<int:event_id>')
