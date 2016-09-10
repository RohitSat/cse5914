import itertools

from flask import g, request, render_template, json

from brutus_module_math import app


@app.route('/')
def index():
    """
    Get the index page.
    """

    return "Brutus Math Module"


@app.route('/api/request', methods=['GET', 'POST'])
def create_request():
    """
    Get requests or create a new request.
    """

    if request.method == 'GET':
        # return requests and their status
        return json.jsonify([
            {'key': 'value'},
            {'key': 'value'}
        ])

    # TODO: do work
    return json.jsonify({'key': 'value'})


@app.route('/api/request/<int:request_id>')
def get_request(request_id):
    """
    Get a request.
    """

    # TODO: do work
    return json.jsonify({
        'id': 3,
        'state': 'pending',
        'request': {
            'text': 'what is the time?'
        }
    })
