from datetime import datetime
from cred.app import db


class Client(db.Model):
    __tablename__ = 'client'
    client_id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(240))
    location = db.Column(db.String(240))
    session = db.Column(db.String(240))
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    apikey_id = db.Column(db.Integer, db.ForeignKey('apikey.apikey_id'))

    def __init__(self, device, location, session, apikey, active=None):
        self.device = device
        self.location = location
        self.session = session
        self.apikey = apikey
        if active is not None:
            self.last_active = active

    def __repr__(self):
        return '<Device %r, Location %r, Last Active %r>' % (
            self.device,
            self.location,
            self.last_active
        )
