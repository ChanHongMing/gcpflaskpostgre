from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import psycopg2
from urllib.parse import urlparse
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

# Set a secret key for the session
app.secret_key = 'your-secret-key'

# Parse the database URL to get connection details
url = urlparse("postgres://zgirpxwy:cvDpInHGHTj0OovWFU5QJEkrX4Bv4X21@tiny.db.elephantsql.com/zgirpxwy")
conn = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:],
    user=url.username,
    password=url.password
)

auth = HTTPBasicAuth()

users = {
    "admin": "password",
    "user": "password"
}

@app.route('/')
def home():
    return render_template('home.html')

@auth.verify_password
def verify_password(username, password):
    if username in users and password == users[username]:
        return username

@app.route('/protected')
@auth.login_required
def protected():
    return jsonify({'message': 'You are authorized to access this API'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_password(username, password):
            # Set the session username and redirect to the index page
            session['username'] = username
            return redirect(url_for('index'))
        else:
            # If the username or password is incorrect, return an error message
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    else:
        # If the request is a GET request, render the login template
        return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session and redirect to the login page
    session.clear()
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'username' not in session:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('login'))
    else:
        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a SELECT statement to retrieve data from the database
        cur.execute("SELECT * FROM users")

        # Fetch all rows from the result set
        rows = cur.fetchall()

        # Close the cursor and database connection
        cur.close()

        # Render the template with the retrieved data
        return render_template('index.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
