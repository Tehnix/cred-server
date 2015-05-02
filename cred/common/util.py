from flask_restful import reqparse
from cred import app, db


parser = reqparse.RequestParser()
parser.add_argument(
    'sessionKey',
    type=str,
    required=True,
    location='cookies',
    help="A session key is required!")

