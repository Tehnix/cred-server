"""
Set up the Flask application, API and database for
the flask server.

"""
import os
from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder


class CustomApi(Api):
    """Extend the base Api class with a custom error handler."""

    def handle_error(self, e):
        """Handle custom exceptions."""
        # If it's an unchaught 500 error, catch it with exceptions
        if getattr(e, 'code', 500) == 500:
            try:
                return self.make_response({
                    'status': e.status,
                    'message': e.message
                }, e.status)
            except Exception as e:
                return super(CustomAPI, self).handle_error(e)
        # Else return the default response
        return super(CustomAPI, self).handle_error(e)


# Create our Application
app = Flask('cred-server')

# Tie the Application to our API
api = CustomApi(app)

# Database
db = SQLAlchemy(app)


# Import all the models, so that when we create the db, we
# create it with the actual tables we need
from cred.models import *


def initDB():
    """Create the database tables."""
    db.create_all()

# Import the routes here, to avoid circular imports
import cred.routes


def run(config):
    cdb = config['database']
    if cdb['type'] == 'sqlite3':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(cdb['database'])
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = '{0}//{1}:{2}@{3}:{4}/{5}'.format(
            cdb['type'],
            cdb['user'],
            cdb['password'],
            cdb['host'],
            cdb['port'],
            cdb['database']
        )
    initDB()
    host = config['host']
    if host == '*':
        host = '0.0.0.0'
    app.run(host=host, port=config['port'])


def run_test():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cred-test.db'
    initDB()
    app.run(debug=True)

if __name__ == '__main__':
    run_test()
