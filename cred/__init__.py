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

# Tie the Application to our API
api = Api(app)

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
