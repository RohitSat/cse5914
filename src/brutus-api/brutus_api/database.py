import sqlite3


def connect_db(filename):
    """
    Connect to the database.
    """

    db = sqlite3.connect(filename)
    db.row_factory = sqlite3.Row

    return db


def query_db(db, query, args=(), single=False):
    """
    Query the database and return the results.
    """

    cursor = db.execute(query, args)
    rows = cursor.fetchall()
    cursor.close()

    return (rows[0] if rows else None) if single else rows


def insert_db(db, query, args=()):
    """
    Insert into the database and return the last row primary key.
    """

    cursor = db.execute(query, args)
    lastrowid = cursor.lastrowid
    cursor.close()

    return lastrowid
