from datetime import datetime
from cred.database import db


class APIKey(db.Model):
    __tablename__ = 'apikey'
    id = db.Column(db.Integer, primary_key=True)
    apikey = db.Column(db.String(240))
    permission = db.Column(db.String(240))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    client = db.relationship(
        'Client',
        backref=db.backref('apikey', uselist=False)
    )

    def __init__(self, apikey, permission='read'):
        self.apikey = apikey
        self.permission = permission

    def __repr__(self):
        return '<ID %r, API Key %r, Permission %r, Created %r>' % (
            self.id,
            self.apikey,
            self.permission,
            self.created
        )
