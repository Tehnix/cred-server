"""
Set up the Flask application, API and database for
the flask server.

"""
import os
import flask
import flask.ext.restful
import flask.ext.sqlalchemy
import flask.ext.cors
import cred.config
import cred.database
from cred.routes import create_api_resources


class CustomApi(flask.ext.restful.Api):
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
app = flask.Flask(__name__)
# Tie the Application to our API
api = CustomApi(app)
# Allow CORS
cors = flask.ext.cors.CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})


def run(config, debug):
    cred.config.loaded_configuration = config
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
    # Create our database
    cred.database.db = flask.ext.sqlalchemy.SQLAlchemy(app)
    cred.database.init_db(cred.database.db)
    # Tie the API endpoints to the correct resources
    create_api_resources(api)
    # Set up the server to listen on the configurated host and port
    host = config['host']
    if host == '*':
        host = '0.0.0.0'
    app.run(host=host, port=config['port'], debug=debug)


if __name__ == '__main__':
    import cred.config
    run(cred.config.default_config, True)
