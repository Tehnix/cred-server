# The db object is used as a singleton throughout the application
db = None


def init_db(db):
    """Import the Models and create the database tables."""
    from cred.models.apikey import APIKey
    from cred.models.client import Client
    from cred.models.event import Event
    from cred.models.subscribe import Subscribe
    db.create_all()
    db.session.commit()
