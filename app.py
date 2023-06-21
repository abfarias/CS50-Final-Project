from flask import Flask, flash, jsonify, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, query_db

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.teardown_appcontext
def close_connection(exception):
    """Close database connection at the end of request"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST', 'DELETE'])
@login_required
def index():
    """Show passwords vault"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':

        # Ensure username was submitted
        if not request.form.get('username'):
            flash('Username is missing!', 'warning')
            return redirect('/')

        # Ensure domain was submitted
        elif not request.form.get('domain'):
            flash('Domain is missing!', 'warning')
            return redirect('/')

        # Ensure password was submitted
        elif not request.form.get('password'):
            flash('Password is missing!', 'warning')
            return redirect('')

        # Save it into the database
        username = request.form.get('username')
        domain = request.form.get('domain')
        password = request.form.get('password')

        query_db('INSERT INTO passwords (user_id, username, domain, hash) VALUES (?, ?, ?, ?)', [session['user_id'], username, domain, password])
        
        # Redirect user to home page
        flash('Password saved!', 'success')
        return redirect('/')

    # User reached route via DELETE
    elif request.method == 'DELETE':
        delete_info = request.get_json()
        
        if delete_info is not None:
            query_db("DELETE FROM passwords WHERE id = ?", [delete_info['id']])
            flash('Password deleted!', 'danger')
            return jsonify({'success': True}), 200
        
        else:
            return redirect('/')
       
    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Get updated list of passwords
        passwords = query_db("SELECT id, username, domain, hash FROM passwords WHERE user_id = ?", [session['user_id']])

        return render_template('index.html', passwords=passwords)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':

        # Ensure username was submitted
        if not request.form.get('username'):
            flash('Username is missing!', 'warning')
            return render_template('register.html')

        # Ensure password was submitted
        elif not request.form.get('password'):
            flash('Password is missing!', 'warning')
            return render_template('register.html')

        # Ensure password confirmation was submitted
        elif not request.form.get('confirmation'):
            flash('Password must be confirmed!', 'warning')
            return render_template('register.html')

        # Ensure password confirmation matches password
        elif request.form.get('password') != request.form.get('confirmation'):
            flash('Passwords does not match!', 'danger')
            return render_template('register.html')

        # Ensure username is available
        count = query_db('SELECT COUNT() FROM users WHERE username = ?', [request.form.get('username')])
        if count[0]['COUNT()'] == 1:
            flash('Username is already taken!', 'warning')
            return render_template('register.html')

        # Store the username and hashed password into the database
        username = request.form.get('username')
        hash = generate_password_hash(request.form.get('password'))

        query_db('INSERT INTO users (username, hash) VALUES(?, ?)', [username, hash])

        # Remember which user has register
        id = query_db('SELECT id FROM users WHERE username = ? AND user_id = ?', [username, session['user_id']])

        session['user_id'] = id[0]['id']

        # Redirect user to home page
        flash('Registered!', 'primary')
        return redirect('/')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('register.html')
     

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
     
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':

        # Ensure username was submitted
        if not request.form.get('username'):
            flash('Username is missing!', 'warning')
            return render_template('login.html')

        # Ensure password was submitted
        elif not request.form.get('password'):
            flash('Password is missing!', 'warning')
            return render_template('login.html')

        # Query database for username
        rows = query_db('SELECT * FROM users WHERE username = ?', [request.form.get('username')])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]['hash'], request.form.get('password')):
            flash('Username or password does not match!', 'danger')
            return render_template('login.html')

        # Remember which user has logged in
        session['user_id'] = rows[0]['id']

        # Redirect user to home page
        return redirect('/')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Log user out"""
    
    # Forget current user_id
    session.clear()

    # Redirect user to login form
    return redirect('/')
