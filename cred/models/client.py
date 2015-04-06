from cred import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(240))
    location = db.Column(db.String(240))
    session = db.Column(db.String(240))

    def __init__(self, device, location, session):
        self.device = device
        self.location = location
        self.session = session

    def __repr__(self):
        return '<Device %r, Location %r' % (self.device, self.location)

