import sqlite3
from flask import redirect, session, g
from functools import wraps

ALLOWED_EXTENSIONS = {'csv'}

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
    g._database.commit()
    return (rv[0] if rv else None) if one else rv

# End of Flask configuration for sqlite3 usage
# https://flask.palletsprojects.com/en/2.3.x/patterns/sqlite3/


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def allowed_extensions(filename: str):
    """
    Checks if file extension is allowed

    https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
    """
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def valid_password(password: str, min_length=12, max_length=64):
    """
    Checks if password meets certain parameters
    """
    if len(password) < min_length or len(password) > max_length:
        return False
    
    special = "~`!@#$%^&*()-_+={[}]|\/:;'<>,.?"
    
    has_uppercase = False
    has_lowercase = False
    has_digit = False
    has_special = False

    for letter in password:
        if letter.isupper():
            has_uppercase = True
        elif letter.islower():
            has_lowercase = True
        elif letter.isdigit():
            has_digit = True
        elif letter in special:
            has_special = True

    return has_uppercase and has_lowercase and has_digit and has_special