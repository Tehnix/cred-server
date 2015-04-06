from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument(
    'apiKey',
    type=str,
    required=True,
    location='json',
    help="API key is required!")

