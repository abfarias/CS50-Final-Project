import sqlite3
from flask import g


# Start of Flask configuration for sqlite3 usage
DATABASE = 'safepass.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    
    # Return rows as dictonaries instead of tuples
    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

    db.row_factory = make_dicts
    
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# End of Flask configuration for sqlite3 usage
# For detailed information acess:https://flask.palletsprojects.com/en/2.3.x/patterns/sqlite3/
