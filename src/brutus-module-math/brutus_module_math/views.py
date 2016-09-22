import itertools

from flask import g, request, render_template, json

from brutus_module_math import app

from brutus_module_math import nlCalc


@app.route('/')
def index():
    """
    Get the index page.
    """

    return "Brutus Math Module"


@app.route('/api/request', methods=['POST'])
def create_request():
    """
    Get requests or create a new request.
    """
    data=request.get_json()
    input_data=data['input']
    contents=input_data['text']
    # 'what is ten plus ten'
    resultstring=nlCalc.calculate(contents)

    result={"input": input_data, 'output':{'text': resultstring}}   
    # TODO: do work
    return json.jsonify(result)


