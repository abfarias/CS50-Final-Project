import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session, g
from flask_session import Session
from security import generate_hash, check_password, check_rehash, derive_key, encrypt, decrypt
from cryptography.fernet import Fernet
from helpers import login_required, query_db

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Server Fernet key
server_key = Fernet(b'EpI8xrilovVLxd3QwMtEM5Pwbkwyb4JeXulio3JAnjE=')


@app.teardown_appcontext
def close_connection(exception):
    """Close database connection at the end of request"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST', 'DELETE', 'UPDATE'])
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
            return redirect('/')

        # Encrypt data
        user_key = Fernet(session['user_key'])

        username = encrypt(user_key, request.form.get('username', type=str))
        domain = encrypt(user_key, request.form.get('domain', type=str))
        password = encrypt(user_key, request.form.get('password', type=str))

        # Save it into the database
        query_db('INSERT INTO passwords (user_id, username, domain, hash) VALUES (?, ?, ?, ?)', [session['user_id'], username, domain, password])
        
        # Redirect user to home page
        flash('Password saved!', 'success')
        return redirect('/')

    # User reached route via DELETE
    elif request.method == 'DELETE':
        delete_info = request.get_json()
        
        if delete_info is not None:
            query_db('DELETE FROM passwords WHERE id = ?', [delete_info['id']])
            flash('Password deleted!', 'danger')
            return jsonify({'success': True}), 200
        
        else:
            return redirect('/')
    
    # User reached route via UPDATE
    elif request.method == 'UPDATE':
        update_info = request.get_json()

        # Search database for corresponding item
        if update_info is not None:

            # Encrypt updated info
            user_key = Fernet(session['user_key'])

            domain = encrypt(user_key, update_info['domain'])
            username = encrypt(user_key, update_info['username'])
            password = encrypt(user_key, update_info['password'])

            # Insert encrypted info into the database
            query_db('UPDATE passwords SET username = ?,  domain = ?,  hash = ? WHERE id = ?', [username, domain, password, update_info['id']])

            flash('Password updated!', 'success')
            return jsonify({'success': True}), 200
        
        else:
            return redirect('/')

       
    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Get updated list of passwords
        list = query_db("SELECT id, username, domain, hash FROM passwords WHERE user_id = ?", [session['user_id']])

        # Decrypt list items
        user_key = Fernet(session['user_key'])

        for item in list:
            item['username'] = decrypt(user_key, item['username']).decode('utf-8')
            item['domain'] = decrypt(user_key, item['domain']).decode('utf-8')
            item['hash'] = decrypt(user_key, item['hash']).decode('utf-8')

        return render_template('index.html', list=list)
    

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

        # Ensure master password was submitted
        elif not request.form.get('master_password'):
            flash('Master password is missing!', 'warning')
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

        # Derive encryption from master password
        salt = os.urandom(16)
        key = derive_key(request.form.get('master_password', type=str), salt) 
        
        session['user_key'] = key

        # Store the username, hashed passwords and encrypted salt into the database
        username = request.form.get('username')
        hash = generate_hash(request.form.get('password'))
        m_hash = generate_hash(request.form.get('master_password'))
        encrypted_salt = server_key.encrypt(salt)

        query_db('INSERT INTO users (username, hash, m_hash, salt) VALUES(?, ?, ?, ?)', [username, hash, m_hash, encrypted_salt])

        # Remember which user has register
        id = query_db('SELECT id FROM users WHERE username = ?', [username], True)

        session['user_id'] = id['id']

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
        
         # Ensure master password was submitted
        elif not request.form.get('master_password'):
            flash('Master password is missing!', 'warning')
            return render_template('login.html')

        # Query database for username
        rows = query_db('SELECT * FROM users WHERE username = ?', [request.form.get('username')])

        # Ensure username exists and passwords are correct
        if len(rows) != 1 or not check_password(rows[0]['hash'], request.form.get('password')) or not check_password(rows[0]['m_hash'], request.form.get('master_password')):
            flash('Username or passwords does not match!', 'danger')
            return render_template('login.html')

        # Remember which user has logged in
        session['user_id'] = rows[0]['id']

        # Derive same encryption key generated in /register from master password
        encrypted_salt = query_db('SELECT salt FROM users WHERE id = ?', [session['user_id']], True)
        salt = decrypt(server_key, encrypted_salt['salt'])
        
        key = derive_key(request.form.get('master_password', type=str), salt) 
        
        session['user_key'] = key

        # Ensure hash is up to date
        if check_rehash(rows[0]['hash']):
            new_hash = generate_hash(request.form.get('password'))
            query_db('UPDATE users SET hash = ? WHERE id = ?', [new_hash, session['user_id']])
        elif check_rehash(rows[0]['m_hash']):
            new_m_hash = generate_hash(request.form.get('master_password'))
            query_db('UPDATE users SET m_hash = ? WHERE id = ?', [new_m_hash, session['user_id']]) 

        # Redirect user to home page
        return redirect('/')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')
    

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':

        # Ensure previous password was submitted
        if not request.form.get('previous_password'):
            flash('Missing previous password!', 'warning')
            return render_template('change_password.html')
        
        # Ensure new password was submitted
        elif not request.form.get('new_password'):
            flash('Missing new password!', 'warning')
            return render_template('change_password.html')

        # Ensure new password confirmation was submitted
        elif not request.form.get('confirmation'):
            flash('Missing new password confirmation!', 'warning')
            return render_template('change_password.html')
        
        # Ensure new password confirmation matches
        elif request.form.get('new_password') != request.form.get('confirmation'):
            flash('Password confirmation does not match!', 'warning')
            return render_template('change_password.html')
        
        # Ensure previous password exists in the database
        hash = query_db('SELECT hash FROM users WHERE id = ?', [session['user_id']], True)

        if not check_password(hash['hash'], request.form.get('previous_password')):
            flash('Previous password does not match!', 'danger')
            return render_template('change_password.html')
        
        # Update previous password
        new_hash = generate_hash(request.form.get('new_password'))

        query_db('UPDATE users SET hash = ? WHERE id = ?', [new_hash, session['user_id']])

        # Disconnect user and redirect to login page
        return redirect('/logout')
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('change_password.html')
    

@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    
    if request.method == 'POST':
         
        # Ensure username was submitted
        if not request.form.get('username'):
            flash('Username is missing!', 'warning')
            return render_template('delete_account.html')

        # Ensure password was submitted
        elif not request.form.get('password'):
            flash('Password is missing!', 'warning')
            return render_template('delete_account.html')
        
         # Ensure master password was submitted
        elif not request.form.get('master_password'):
            flash('Master password is missing!', 'warning')
            return render_template('delete_account.html')

        # Query database for username
        rows = query_db('SELECT * FROM users WHERE username = ?', [request.form.get('username')])

        # Ensure username exists and passwords are correct
        if len(rows) != 1 or not check_password(rows[0]['hash'], request.form.get('password')) or not check_password(rows[0]['m_hash'], request.form.get('master_password')):
            flash('Username or passwords does not match!', 'danger')
            return render_template('delete_account.html')
        
        # Delete user data
        query_db('DELETE FROM passwords WHERE user_id = ?', [session['user_id']])
        query_db('DELETE FROM users WHERE id = ?', [session['user_id']])

        # Disconnect user and redirect to login page
        return redirect('/logout')
    else:
        return render_template('delete_account.html')


@app.route('/logout')
@login_required
def logout():
    """Log user out"""
    
    # Forget current user_id
    session.clear()

    # Redirect user to login form
    return redirect('/')
