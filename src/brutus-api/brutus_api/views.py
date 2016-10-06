import itertools

from flask import g, request, render_template, json, abort

from brutus_api import app
from brutus_api.tasks import get_answer

from .database import query_db


def format_request(data):
    job = g.queue.fetch_job(str(data['job_id']))
    request = {
        'id': data['id'],
        'job_id': data['job_id'],
        'module_id': data['module_id'],
        'status': None if job is None else job.get_status(),
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


@app.route('/api/request', methods=['GET', 'POST'])
def create_request():
    """
    Get requests or create a new request.
    """

    if request.method == 'GET':
        # retrieve all requests
        requests = map(format_request, query_db('SELECT * FROM request'))

        # return requests and their status
        return json.jsonify(list(requests))

    # XXX
    data = request.get_json()

    # store the request details in the database
    cursor = g.db.cursor()
    cursor.execute(
        'INSERT INTO request (status, input) VALUES (?, ?)',
        ('created', data['text']))

    g.db.commit()

    # XXX
    request_id = cursor.lastrowid
    job = g.queue.enqueue(get_answer, request_id)

    # XXX
    cursor.execute(
        'UPDATE request SET job_id = ? WHERE id = ?',
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
