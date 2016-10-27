import itertools

from flask import g, request, render_template, json

from brutus_module_jokes import app
from .tasks import find_document


@app.route('/')
def index():
    """
    Get the index page.
    """

    return "Brutus Jokes Module"


@app.route('/api/request', methods=['POST'])
def create_request():
    """
    Get requests or create a new request.
    """

    data = request.get_json()
    input_data = data['input']
    resultstring = find_document(input_data['text'])
    result = {"input": input_data, 'output': {'text': resultstring}}
    return json.jsonify(result)
