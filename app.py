import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug import url_quote

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the template directory path
template_dir = os.path.join(current_dir, 'templates')

# Initialize Flask app with the template directory
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'password'  # Change this to a random secret key

# Mock database for storing users
users = {'admin': generate_password_hash('admin')}  # Pre-populate with an admin user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return 'User already exists!'
        users[username] = generate_password_hash(password)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users or not check_password_hash(users[username], password):
            return 'Invalid username or password'
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('profile'))
    return render_template('login.html')


@app.route('/profile')
def profile():
    if 'logged_in' in session:
        return f'Welcome, {session["username"]}!'
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
