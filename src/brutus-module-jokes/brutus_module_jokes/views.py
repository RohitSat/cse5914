import sqlite3
import itertools

from flask import g, request, render_template, json

from brutus_module_jokes import app
from .database import connect_db, query_db


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
    past_data = data['data']

    db = connect_db(app.config['DATABASE'])
    joke = query_db(
            db, 
            'SELECT * FROM jokes ORDER BY RANDOM() LIMIT 1;',
            (),
            single=True) 

    if(request is None):
        raise RuntimeError("joke {0} not found".format(joke_id))

    jokeId = joke['id'] 
    joke = query_db(
            db, 
            'SELECT * FROM jokes_parts where jokeId = ? ORDER BY id;',
            (jokeId, ),
            ) 

    # result = {"input": input_data, 'output': {'text': j }, 'data' : { 'joke' : 'this is an example' }
    result = {'input': input_data, 'output': {'text': j } }
    return json.jsonify(result)
