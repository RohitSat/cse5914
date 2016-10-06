import os
import sys
import uuid
import sqlite3
import itertools

from flask import Flask, g
from flask_cors import CORS
from rq import Queue
from rq.registry import StartedJobRegistry, FinishedJobRegistry
from redis import Redis


# create the flask application
app = Flask(__name__)


app.config.update(
    DEBUG=os.getenv('DEBUG', 'False') in ['true', 'True'],
    SECRET_KEY=os.getenv('SECRET_KEY', str(uuid.uuid4())),
    REDIS_HOST=os.getenv('REDIS_HOST', '127.0.0.1'),
    REDIS_PORT=int(os.getenv('REDIS_PORT', '6379')),
    REDIS_DB=int(os.getenv('REDIS_DB', '0')),
    DATABASE=os.getenv('DATABASE', '/tmp/brutus.db'),
    NLC_WATSON_USERNAME=os.getenv('NLC_WATSON_USERNAME'),
    NLC_WATSON_PASSWORD=os.getenv('NLC_WATSON_PASSWORD'),
    NLC_CLASSIFIER_NAME=os.getenv('BRUTUS_API_NLC_CLASSIFIER'))


# enable CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# XXX
from .database import get_db, init_db


# register event handlers
@app.before_request
def connect_database():
    """
    Connect to the SQLite3 database and store the connection in the application
    context.
    """

    # check if the database file already exists
    db_file_present = not os.path.isfile(app.config['DATABASE'])

    # connect to the database
    g.db = get_db()

    # initialize the schema if the database file did not already exist
    if not db_file_present:
        init_db()


@app.teardown_appcontext
def disconnect_database(exception):
    """
    Disconnect from the SQlite3 database if we're currently connected.
    """

    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.before_request
def connect_redis():
    """
    Connect to Redis and store the connection for in the application
    context.
    """

    g.redis = Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'])

    g.queue = Queue(connection=g.redis)
    g.started_registry = StartedJobRegistry(connection=g.redis)
    g.finished_registry = FinishedJobRegistry(connection=g.redis)
