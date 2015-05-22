"""
Custom exceptions used to handle common states of the API.

"""


class NotAuthenticated(Exception):
    status = 401
    message = 'Not Authenticated'


class InvalidAPIKey(Exception):
    status = 401
    message = 'Invalid API Key'
    

class InsufficientPermissions(Exception):
    status = 403
    message = "Insufficient Permissions"


class InvalidPermissions(Exception):
    status = 400
    message = "Invalid Permissions"


class ClientNotFound(Exception):
    status = 404
    message = 'Client Not Found'


class EventNotFound(Exception):
    status = 404
    message = 'Event Not Found'


class APIKeyNotFound(Exception):
    status = 404
    message = 'API Key Not Found'
