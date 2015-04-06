from cred import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(240))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship(
        'Client',
        backref=db.backref('events', lazy='dynamic'))

    def __init__(self, event, client):
        self.event = event
        self.client = client

    def __repr__(self):
        return '<Event %r, Client %r' % (self.event, self.client.device)

