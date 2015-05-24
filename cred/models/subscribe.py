from cred.database import db


class Subscribe(db.Model):
    __tablename__ = 'subscribe'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(240))
    location = db.Column(db.String(240))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship(
        'Client',
        backref=db.backref('subscribes', lazy='dynamic'))

    def __init__(self, client, event, location):
        self.client = client
        self.event = event
        self.location = location

    def __repr__(self):
        return '<Client %r, Event %r, Location %r>' % (
            self.client.device,
            self.event,
            self.location
        )
