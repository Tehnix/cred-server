from cred import db

class RegisteredEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship(
        'Client',
        backref=db.backref('registered_events', lazy='dynamic'))

    def __init__(self, client, name):
        self.client = client
        self.name = name

    def __repr__(self):
        return self.name

