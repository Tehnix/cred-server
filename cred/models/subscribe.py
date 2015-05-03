from cred import db


class Subscribe(db.Model):
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
