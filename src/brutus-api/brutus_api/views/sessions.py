from flask import g, request, json, abort

from brutus_api.app import app
from brutus_api.database import query_db


@app.route('/api/session')
def sessions():
    """
    Get sessions.
    """

    # retrieve all modules
    sessions = map(dict, query_db(g.db, 'SELECT * FROM session'))
    return json.jsonify(list(sessions))


@app.route('/api/session/<int:session_id>')
def get_session(session_id):
    """
    Get a session.
    """

    # retrieve the session
    session = query_db(
        g.db,
        'SELECT * FROM session WHERE id = ?',
        (session_id, ),
        single=True)

    if session is None:
        # session not found
        abort(404)

    # return the module data
    return json.jsonify(dict(session))
