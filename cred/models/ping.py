from datetime import datetime
from cred import db


class Ping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship(
        'Client',
        backref=db.backref('pings', lazy='dynamic'))

    def __init__(self, client, time=None):
        self.client = client
        if time is None:
            time = datetime.utcnow()
        self.time = time

    def __repr__(self):
        return '<Time %r, Client %r' % (self.time, self.client.device)

