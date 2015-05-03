from datetime import datetime
from cred import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(240))
    location = db.Column(db.String(240))
    session = db.Column(db.String(240))
    last_active = db.Column(db.DateTime)
    last_pull = db.Column(db.DateTime)

    def __init__(self, device, location, session, active=None, pull=None):
        self.device = device
        self.location = location
        self.session = session
        if active is None:
            active = datetime.utcnow()
        self.last_active = active
        if pull is None:
            pull = datetime.utcnow()
        self.last_pull = pull

    def __repr__(self):
        return '<Device %r, Location %r' % (self.device, self.location)
