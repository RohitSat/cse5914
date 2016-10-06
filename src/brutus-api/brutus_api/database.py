import sqlite3

from flask import g

from .app import app


def get_db():
    """
    Connect to the database.
    """

    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row

    return db


def init_db():
    """
    Create the database tables.
    """

    with app.open_resource('schema.sql', mode='r') as schema_file:
        schema_sql = schema_file.read()
        get_db().cursor().executescript(schema_sql)


def query_db(query, args=(), single=False):
    """
    Query the database and return the results.
    """

    cursor = get_db().execute(query, args)
    rows = cursor.fetchall()
    cursor.close()

    return (rows[0] if rows else None) if single else rows
