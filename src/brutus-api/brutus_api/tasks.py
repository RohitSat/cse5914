import sqlite3
import requests
from redis import Redis
from rq import get_current_job
from flask import json

from .app import app
from .nlp import Nlp
from .database import connect_db, query_db


def process_request(request_id):
    """
    get the answer for a question asked by the user
        -find the module
        -wait for the module to respond
        -set the result
    """

    # connect to the database
    db = connect_db(app.config['DATABASE'])

    # get the current job
    redis = Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'])

    job = get_current_job(connection=redis)

    # get the current request
    request = query_db(
        db,
        'SELECT * FROM request WHERE id = ?',
        (request_id, ),
        single=True)

    if request is None:
        raise RuntimeError("request {0} not found".format(request_id))

    # set up natural language processor object and pass it the classifier name
    nlc = Nlp(
        app.config['NLC_WATSON_USERNAME'],
        app.config['NLC_WATSON_PASSWORD'],
        app.config['NLC_CLASSIFIER_NAME'])

    # XXX get the module
    module_name = nlc.classify(request['input'])
    module = query_db(
        db,
        'SELECT * FROM module WHERE name = ?',
        (module_name, ),
        single=True)

    if module is None:
        raise RuntimeError("module {0} not found".format(module_name))

    # XXX
    db.execute(
        'UPDATE request SET module_id = ? WHERE id = ?',
        (module['id'], request_id))

    db.commit()

    # query the module
    r = requests.post(
        "{0}/api/request".format(module['url']),
        json={'input': {'text': request['input']}})

    if r.text is not None:
        result = json.loads(r.text)
        output = result['output']

    else:
        output = {'text': 'An error occured processing your request.'}

    # XXX
    db.execute(
        'UPDATE request SET output = ? WHERE id = ?',
        (output['text'], request_id))

    db.commit()
