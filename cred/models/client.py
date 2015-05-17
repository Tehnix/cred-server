from datetime import datetime
from cred import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(240))
    location = db.Column(db.String(240))
    session = db.Column(db.String(240))
    last_active = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, device, location, session, active=None):
        self.device = device
        self.location = location
        self.session = session
        if active is None:
            active = datetime.utcnow()
        self.last_active = active

    def __repr__(self):
        return '<Device %r, Location %r, Last Pull %r, Last Active %r>' % (
            self.device,
            self.location,
            self.last_active
        )
