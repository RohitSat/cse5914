import itertools

from flask import g, request, render_template, json

from brutus_api import app
from brutus_api.tasks import create_profile


@app.route('/')
def index():
    """
    Get the index page.
    """

    return "Hello, World!"

@app.route('/api/request', methods=['GET', 'POST'])
def create_request():
    """
    Get requests or create a new request.
    """

    if request.method == 'GET':
        # return requests and their status
        return json.jsonify([
            {
                'id': 1,
                'state': 'pending',
                'request': {
                    'text': 'what is 7 cm in meters?'
                }
            },
            {
                'id': 2,
                'state': 'done',
                'request': {
                    'text': 'what is 3 + 4?'
                },
                'result': {
                    'say': 'the answer is 7'
                }
            }
        ])

    # TODO: do work
    return josn.jsonify({
        'id': 3,
        'state': 'pending',
        'request': {
            'text': 'what is the time?'
        }
    })

@app.route('/api/request/<int:request_id>')
def get_request(request_id):
    """
    Get a request.
    """

    # TODO: do work
    return josn.jsonify({
        'id': 3,
        'state': 'pending',
        'request': {
            'text': 'what is the time?'
        }
    })
