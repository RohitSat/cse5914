from flask import g, request, render_template, json, abort

from brutus_api.app import app
from brutus_api.tasks import process_request
from brutus_api.database import query_db, insert_db


def format_request(data):
    """
    Convert raw request data into the format exposed by the API.
    """

    # format the request data
    request = {
        'id': data['id'],
        'status': data['status'],
        'session_id': data['session_id'],
        'input': None,
        'output': None}

    if data['input'] is not None:
        request['input'] = {'text': data['input']}

    if data['output'] is not None:
        request['output'] = {'text': data['output']}

    return request


@app.route('/api/request', methods=['GET', 'POST'])
def requests():
    """
    Get requests or create a new request.
    """

    if request.method == 'GET':
        # retrieve all requests
        requests = map(format_request, query_db(g.db, 'SELECT * FROM request'))
        return json.jsonify(list(requests))

    # check if we need to create a session
    input_data = request.get_json()
    if 'session_id' in input_data:
        # retrieve the existing session
        session_id = input_data['session_id']
        session = query_db(
            g.db,
            'SELECT * FROM session WHERE id = ?',
            (session_id, ),
            single=True)

        if session is None:
            # need to use a session id for an existing session
            abort(400)

        if session['status'] != 'open':
            # need to use an open session
            abort(400)

    else:
        # create a new session
        session_id = insert_db(
            g.db,
            'INSERT INTO session (status) VALUES (?)',
            ('open', ))

    # create the request in the database
    request_id = insert_db(
        g.db,
        'INSERT INTO request (session_id, status, input) VALUES (?, ?)',
        (session_id, 'created', input_data['text']))

    g.db.commit()

    # create the background job and update the request
    job = g.queue.enqueue(process_request, request_id)
    g.db.execute(
        'UPDATE request SET status = \'queued\', job_id = ? WHERE id = ?',
        (job.id, request_id))

    g.db.commit()

    # return the initial request data
    return json.jsonify({
        'id': request_id,
        'job_id': job.id,
        'session_id': session_id,
        'status': job.get_status(),
        'input': {'text': input_data['text']},
        'output': None})


@app.route('/api/request/<int:req_id>')
def get_request(req_id):
    """
    Get a request.
    """

    # retrieve the request
    request = query_db(
        g.db,
        'SELECT * FROM request WHERE id = ?',
        (req_id, ),
        single=True)

    if request is None:
        # request not found
        abort(404)

    # return the request data
    return json.jsonify(format_request(request))
