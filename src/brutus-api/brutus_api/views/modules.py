from flask import g, request, json, abort

from brutus_api.app import app
from brutus_api.database import query_db, insert_db


@app.route('/api/module', methods=['GET', 'POST'])
def modules():
    """
    Get configured modules.
    """

    if request.method == 'GET':
        # retrieve all modules
        modules = map(dict, query_db(g.db, 'SELECT * FROM module'))
        return json.jsonify(list(modules))

    # create the module in the database
    input_data = request.get_json()
    module_id = insert_db(
        g.db,
        'INSERT INTO module (name, url) VALUES (?, ?)',
        (input_data['name'], input_data['url']))

    g.db.commit()

    # return the module data
    return json.jsonify({
        'id': module_id,
        'name': input_data['name'],
        'url': input_data['url']})


@app.route('/api/module/<int:mod_id>')
def get_module(mod_id):
    """
    Get a module.
    """

    # retrieve the module
    module = query_db(
        g.db,
        'SELECT * FROM module WHERE id = ?',
        (mod_id, ),
        single=True)

    if module is None:
        # module not found
        abort(404)

    # return the module data
    return json.jsonify(dict(module))


@app.route('/api/module/<int:mod_id>', methods=['DELETE'])
def delete_module(mod_id):
    """
    Delete a module.
    """

    # retrieve the module
    module = query_db(
        g.db,
        'SELECT * FROM module WHERE id = ?',
        (mod_id, ),
        single=True)

    if module is None:
        # module not found
        abort(404)

    # create a cursor so we can group multiple statements into a transaction
    cursor = g.db.cursor()

    # remove the module from any requests
    cursor.execute(
        'UPDATE request SET module_id = NULL WHERE module_id = ?',
        (mod_id, ))

    # delete the module
    cursor.execute('DELETE FROM module WHERE id = ?', (mod_id, ))

    # commit the transaction
    g.db.commit()

    # return an empty response
    return '', 204
