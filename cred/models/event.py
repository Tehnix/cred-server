from cred import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240))
    location = db.Column(db.String(240))
    action = db.Column(db.String(240))
    value = db.Column(db.String(240))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship(
        'Client',
        backref=db.backref('events', lazy='dynamic'),
        order_by=id)

    def __init__(self, client, name, location, action, value):
        self.client = client
        self.name = name
        self.location = location
        self.action = action
        self.value = value

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'action': self.action,
            'value': self.value
        }

