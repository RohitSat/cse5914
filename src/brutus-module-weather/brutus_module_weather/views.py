import itertools

from flask import g, request, render_template, json

from brutus_module_weather import app


@app.route('/')
def index():
    """
    Get the index page.
    """

    return "Brutus Weather Module"


@app.route('/api/request', methods=['POST'])
def create_request():
    """
    Get requests or create a new request.
    """

    # TODO: do work
    return json.jsonify({'key': 'value'})
