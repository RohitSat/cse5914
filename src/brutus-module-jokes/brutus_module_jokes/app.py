import os
import uuid
import itertools

from flask import Flask, g, request, render_template, json

from .database import connect_db

# create the flask application
app = Flask(__name__)

app.config.update(
    DEBUG=os.getenv('DEBUG', 'False') in ['true', 'True'],
    SECRET_KEY=os.getenv('SECRET_KEY', str(uuid.uuid4())),
    DATABASE=os.getenv('JOKES_DATABASE', '/tmp/jokes.db'),
    RAR_WATSON_USERNAME=os.getenv('RAR_JOKES_USERNAME'),
    RAR_WATSON_PASSWORD=os.getenv('RAR_JOKES_PASSWORD'),
    RAR_WATSON_CLUSTER_ID=os.getenv('RAR_JOKES_CLUSTER_ID'),
    RAR_WATSON_COLLECTION_NAME=os.getenv('RAR_JOKES_COLLECTION_NAME'))


# register event handlers
@app.before_request
def connect_database():
    """
    Connect to the SQLite3 database and store the connection in the application
    context.
    """

    # check if the database file already exists
    database_file_exists = os.path.isfile(app.config['DATABASE'])

    # connect to the database
    g.db = connect_db(app.config['DATABASE'])

    # initialize the database if the file did not exist
    if not database_file_exists:
        with app.open_resource('schema.sql', 'r') as schema_file:
            schema_sql = schema_file.read()

        g.db.executescript(schema_sql)
        g.db.commit()


@app.teardown_appcontext
def disconnect_database(exception):
    """
    Disconnect from the SQlite3 database if we're currently connected.
    """

    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
