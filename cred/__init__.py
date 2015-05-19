"""
Set up the Flask application, API and database for
the flask server.

"""
from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder

SSL = True

# Create our Application
app = Flask(__name__)


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


# Tie the Application to our API
api = CustomApi(app)

# Configure it to use a SQLite DB, using SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test1.db'
db = SQLAlchemy(app)

# Import all the models, so that when we create the db, we
# create it with the actual tables we need
from cred.models import *


def initDB():
    """Create the database tables."""
    db.create_all()

# Import the routes here, to avoid circular imports
import cred.routes
