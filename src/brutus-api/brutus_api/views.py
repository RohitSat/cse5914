import itertools

from flask import g, request, render_template, json, abort

from .app import app
from .tasks import process_request

from .database import query_db, insert_db


def format_request(data):
    module = query_db(
        g.db,
        'SELECT * FROM module WHERE id = ?',
        (data['module_id'], ),
        single=True)

    request = {
        'id': data['id'],
        'status': data['status'],
        'module': None if module is None else module['name'],
        'input': None,
        'output': None}

    if data['input'] is not None:
        request['input'] = {'text': data['input']}

    if data['output'] is not None:
        request['output'] = {'text': data['output']}

    return request


@app.route('/')
def index():
    """
    Get the index page.
    """

    return "Brutus API"


@app.route('/api/module', methods=['GET'])
def modules():
    """
    Get configured modules.
    """

    modules = map(dict, query_db(g.db, 'SELECT * FROM module'))
    return json.jsonify(list(modules))


@app.route('/api/request', methods=['GET', 'POST'])
def requests():
    """
    Get requests or create a new request.
    """

    if request.method == 'GET':
        # retrieve all requests
        requests = map(format_request, query_db(g.db, 'SELECT * FROM request'))

        # return requests and their status
        return json.jsonify(list(requests))

    # XXX
    data = request.get_json()

    # store the request details in the database
    request_id = insert_db(
        g.db,
        'INSERT INTO request (status, input) VALUES (?, ?)',
        ('created', data['text']))

    g.db.commit()

    # XXX
    job = g.queue.enqueue(process_request, request_id)

    # XXX
    g.db.execute(
        'UPDATE request SET status = \'queued\', job_id = ? WHERE id = ?',
        (job.id, request_id))

    g.db.commit()

    # XXX
    data = {
        'id': request_id,
        'job_id': job.id,
        'module_id': None,
        'status': job.get_status(),
        'input': {'text': data['text']},
        'output': None}

    # return the request information
    return json.jsonify(data)


@app.route('/api/request/<int:req_id>')
def get_request(req_id):
    """
    Get a request.
    """

    request = query_db('SELECT * FROM request WHERE id = ?', [req_id], True)
    if request is None:
        abort(404)

    return json.jsonify(format_request(request))
