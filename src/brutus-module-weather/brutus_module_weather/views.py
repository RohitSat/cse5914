import itertools

from flask import g, request, render_template, json

from brutus_module_weather import app

from brutus_module_weather import owmWeather


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

    data = request.get_json()
    input_data = data['input']
    contents = input_data['text']
    # 'what is the weather in columbus ohio'
    resultstring = owmWeather.process_input(contents)

    result = {'input': input_data, 'output': {'text': resultstring}}
    return json.jsonify(result)
