import os
import uuid
import itertools

from flask import Flask, g, request, render_template, json
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
    REDIS_DB=int(os.getenv('REDIS_DB', '0')))
    WATSON_USERNAME='XXXXXXX',
    WATSON_PASSWORD='XXXXXXX'



# register event handlers
@app.before_request
def before_request():
    """
    Initialize the request context.
    """

    g.redis = Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'])

    g.queue = Queue(connection=g.redis)
    g.started_registry = StartedJobRegistry(connection=g.redis)
    g.finished_registry = FinishedJobRegistry(connection=g.redis)
