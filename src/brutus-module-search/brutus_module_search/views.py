import itertools

from flask import g, request, render_template, json

from brutus_module_search import app


@app.route('/')
def index():
    """
    Get the index page.
    """

    return "Brutus Search Module"


@app.route('/api/request', methods=['POST'])
def create_request():
    """
    Get requests or create a new request.
    """
    data = request.get_json()
    input_data = data['input']
    contents = input_data['text']
    resultstring = "the answer will go here!"

    result = {"input": input_data, 'output': {'text': resultstring}}
    return json.jsonify(result)
