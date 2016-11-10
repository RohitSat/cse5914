import sqlite3
from flask import json

from .app import app
import json
from watson_developer_cloud import RetrieveAndRankV1
from .database import connect_db, query_db

def find_joke(question):
    """
    find a joke to tell the user
    """
    # TODO get type of joke 

    db = connect_db(app.config['DATABASE'])
    # joke_type = 'knock knock'
    joke = query_db(
            db, 
            'SELECT * FROM jokes ORDER BY RANDOM() LIMIT 1;',
            (),
            single=True) 

    if(request is None):
        raise RuntimeError("joke {0} not found".format(joke_id))


    return joke['body']
