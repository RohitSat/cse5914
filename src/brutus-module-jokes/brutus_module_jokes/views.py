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
    input_json = request.get_json()
    input_data = input_json['input']

    if 'data' not in input_json:
        db = connect_db(app.config['DATABASE'])
        joke = query_db(
                db, 
                'SELECT * FROM jokes ORDER BY RANDOM() LIMIT 1;',
                (),
                single=True) 

        if(request is None):
            raise RuntimeError("joke {0} not found".format(joke_id))

        jokeId = joke['id'] 
        joke_parts = query_db(
                db, 
                'SELECT * FROM joke_parts where jokeId = ? ORDER BY id;',
                (jokeId, ),
                ) 

        line = joke_parts[0]['part']

        if(len(joke_parts) > 1 ):
            data = []
            for p in joke_parts[1:]:
                data.append(p['part'])

            result = {'input': input_data, 
                     'output': {'text': line },
                     'data' : data }
            return json.jsonify(result)

        result = {'input': input_data, 'output': {'text': line } }
        return json.jsonify(result)

    past_data = input_json['data'] 
    line = past_data[0]
    past_data.pop(0)
    if(len(past_data) > 0):
        result = {'input': input_data, 'output': {'text': line}, 'data' : past_data }
        return json.jsonify(result)
        
    result = {'input': input_data, 'output': {'text': line} }
    return json.jsonify(result)
