from flask import g, request, render_template, json, abort

from brutus_api.app import app
from brutus_api.tasks import process_request
from brutus_api.database import query_db, insert_db


@app.route('/api/module', methods=['GET'])
def modules():
    """
    Get configured modules.
    """

    modules = map(dict, query_db(g.db, 'SELECT * FROM module'))
    return json.jsonify(list(modules))
