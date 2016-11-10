import sqlite3
import requests
from redis import Redis
from rq import get_current_job
from flask import json

from .app import app
from .nlc import Nlc
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

    # get the current session
    session_id = request['session_id']
    session = query_db(
        db,
        'SELECT * FROM session WHERE id = ?',
        (session_id, ),
        single=True)

    if session is None:
        raise RuntimeError("session {0} not found".format(session_id))

    # update the request status
    db.execute(
        "UPDATE request SET status = 'started' WHERE id = ?",
        (request_id, ))

    db.commit()

    try:
        # check if we need to classify the module
        if session['module_id'] is None:
            # classify the module using the natural language classifier
            nlc = Nlc(
                app.config['NLC_WATSON_USERNAME'],
                app.config['NLC_WATSON_PASSWORD'],
                app.config['NLC_CLASSIFIER_NAME'])

            module_name = nlc.classify(request['input'])
            module = query_db(
                db,
                'SELECT * FROM module WHERE name = ?',
                (module_name, ),
                single=True)

            if module is None:
                raise RuntimeError(
                    "module with name {0} not found".format(module_name))

            # update the session module
            db.execute(
                'UPDATE session SET module_id = ? WHERE id = ?',
                (module['id'], session_id))

            db.commit()

        # retrieve the session module
        else:
            module = query_db(
                db,
                'SELECT * FROM module WHERE id = ?',
                (session['module_id'], ),
                single=True)

            if module is None:
                raise RuntimeError(
                    "module {0} not found".format(session['module_id']))

        # query the module
        request_data = {'input': {'text': request['input']}, 'data': {}}
        if session['module_data'] is not None:
            request_data['data'] = json.loads(session['module_data'])

        module_url = "{0}/api/request".format(module['url'])
        response = requests.post(module_url, json=request_data)

        if response.status_code != 200:
            raise RuntimeError(
                "request to {0} module failed".format(module['name']))

        response_data = json.loads(response.text)
        if 'data' in response_data:
            # update the session module data
            db.execute(
                'UPDATE session SET module_data = ? WHERE id = ?',
                (json.dumps(response_data['data']), session_id))

        else:
            # close the session
            db.execute(
                "UPDATE session SET status = 'closed' WHERE id = ?",
                (session_id, ))

        # update the request with a finished state
        db.execute(
            "UPDATE request SET status = 'finished', output = ? WHERE id = ?",
            (response_data['output']['text'], request_id))

        db.commit()

    except Exception as e:
        # update the request with a failed state and generic error message
        db.execute(
            "UPDATE request SET status = 'failed', output = ? WHERE id = ?",
            ("Something went wrong. Try again a little later.", request_id))

        # close the session
        db.execute(
            "UPDATE session SET status = 'closed' WHERE id = ?",
            (session_id, ))

        # commit the changes
        db.commit()

        # stop running
        return
