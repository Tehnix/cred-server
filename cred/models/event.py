from datetime import datetime
from cred.database import db


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240))
    location = db.Column(db.String(240))
    action = db.Column(db.String(240))
    value = db.Column(db.String(240))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship(
        'Client',
        backref=db.backref('events', lazy='dynamic'))

    def __init__(self, client, name, location, action, value, time=None):
        self.client = client
        self.name = name
        self.location = location
        self.action = action
        self.value = value
        if time is not None:
            self.time = time

    def __repr__(self):
        return '<ID %r, Name %r, Location %r, Action %r, Value %r, Time %r>' % (
            self.id,
            self.name,
            self.location,
            self.action,
            self.value,
            self.time
        )
