from flask import Flask, render_template, request, redirect, url_for, flash, session, redirect
import pymysql as MySQLdb
import hashlib
import secrets

# Connect to database
db = MySQLdb.connect(host= input('input MySQL database host: '),
                     user= input('input your username: '),
                     passwd= input('input your password: '),
                     db= input('input the name of your database: '))
cur = db.cursor()  # create cursor on mysqldb

# Create the Flask application
app = Flask(__name__)  
app.secret_key = input('input the secret key for the app: ')


# Function to generate a random recovery key
def generate_recovery_key():
    return secrets.token_urlsafe(20)  # Generate a random URL-safe recovery key

# Function to hash data
def hash_data(data):
    hashed_data = hashlib.sha256(data.encode()).hexdigest()
    return hashed_data

# Function to check if the user is logged in
def check_logged_in():
    return 'logged_in' in session


# Home pages
@app.route('/home/')  
@app.route('/')  
def frontpage():
    return render_template('index.html')


# Login page
@app.route('/login/', methods=['POST', 'GET']) 
def login():
    if request.method == 'POST':
        
        # retreive user inputs
        submitted_username = request.form['username']
        submitted_password = request.form['password']

        # format user inputs to match database
        submitted_username = submitted_username.strip()
        submitted_username = submitted_username.lower()
        hashed_password = hash_data(submitted_password)

        # Check if login credentials exist
        if cur.execute("SELECT * FROM users WHERE usernames = %s AND passwords = %s", (submitted_username,hashed_password)):
            if check_logged_in(): # log user out from previous session
                session.pop('logged_in', None)
                session.pop('username', None)
            session['logged_in'] = True
            session['username'] = submitted_username
            return render_template('login_successful.html')
        else:
            flash('ERROR: Login unsuccessful. Username or password incorrect')

    return render_template('login.html')
    
# Sign-up page
@app.route('/signup/', methods=['POST', 'GET'])  
def signup():
    if request.method == 'POST':

        # clean session data 
        session.pop('new_username', None)
        session.pop('password', None)
        session.pop('recovery_key', None)

        # retreive user inputs
        new_username = request.form['username']
        password = request.form['password']
        re_password = request.form['re_password']
        
        # format inputs to match database
        new_username = new_username.strip()
        password = password.strip()
        re_password = re_password.strip()
        new_username = new_username.lower()
        
        # server side validation
        if password != re_password:
            flash('Re-entered password does not match the password.')
            return render_template('signup.html')
        
        # check if username already in use
        cur.execute("SELECT * FROM users WHERE usernames = %s", (new_username))
        UsernameExist = cur.fetchone()
        if UsernameExist:
            flash('ERROR: Sign up unsuccessful. Username already in use')
            return render_template('signup.html')
        else:
            recovery_key = generate_recovery_key() # generate recovery key
            session['new_username'] = new_username
            session['password'] = password
            session['recovery_key'] = recovery_key
            return render_template('recovery_key.html', recovery_key=recovery_key)
            
    return render_template('signup.html')

# API to verify recovery key
@app.route('/verify_recovery_key/', methods=['POST'])
def verify_recovery_key():
    if request.method == 'POST':
        
        # retreive user inputs from recovery_key page
        entered_recovery_key = request.form['entered_recovery_key']
        
        # remove whitespace from entered recovery key
        entered_recovery_key = entered_recovery_key.strip()

        # retreive user inputs from signup page
        recovery_key = session.get('recovery_key')
        password = session.get('password')
        new_username = session.get('new_username')
        
        # if user input is correct, store credentials in database
        if recovery_key == entered_recovery_key:

            # hash credentials
            hashed_password = hash_data(password)
            hashed_recovery_key = hash_data(recovery_key)

            # store data in database
            cur.execute("INSERT INTO users (usernames, passwords, recovery_keys) VALUES (%s,%s,%s)", (new_username, hashed_password, hashed_recovery_key))
            db.commit()

            # clean session data 
            session.pop('new_username', None)
            session.pop('password', None)
            session.pop('recovery_key', None)

            # redirect user to login page
            return render_template('signup_successful.html')
        else:
            flash('ERROR: Please paste the recovery key correctly.')
            return render_template('recovery_key.html', recovery_key=recovery_key) 
    else:
        return redirect('/404')


# Account recovery
@app.route('/forgot_password/',methods=['POST','GET'])
def forgot_password():
    if request.method == 'POST':

        # clean session tokens
        session.pop('Key_AccountRecovery',None)
        session.pop('Username_AccountRecovery',None)
        
        # retrieve credentials
        username = request.form['username']
        recovery_key = request.form['recovery_key']

        # format credentials to match database
        username = username.lower()
        username = username.strip()
        hashed_recovery_key = hash_data(recovery_key)
        
        # check if credentials are valid
        cur.execute("SELECT * FROM users WHERE usernames = %s AND recovery_keys = %s", (username, hashed_recovery_key))
        check_credentials = cur.fetchone()
        if check_credentials:

            # pass username and hashed key to /reset_password
            session['Key_AccountRecovery'] = hashed_recovery_key
            session['Username_AccountRecovery'] = username
            return render_template('reset_password.html')
        else: 
            flash('Error: Username or recovery key incorrect')
            return render_template('forgot_password.html')
        
    return render_template('forgot_password.html') 

# API to reset password 
@app.route('/reset_password/', methods=['POST'])
def reset_password():
    if request.method == 'POST':

        # retrieve credentials
        new_password = request.form['password']
        re_password = request.form['re_password']
        
        # server side validation
        if new_password == re_password:

            # retreive credentials from /forgot_password
            hashed_recovery_key = session.get('Key_AccountRecovery')
            username = session.get('Username_AccountRecovery')

            # hash the new password
            hashed_new_password = hash_data(new_password)

            # update database
            cur.execute("UPDATE users SET passwords = %s WHERE usernames = %s AND recovery_keys = %s", (hashed_new_password, username, hashed_recovery_key))

            # clean session tokens
            session.pop('Key_AccountRecovery',None)
            session.pop('Username_AccountRecovery',None)

            # redirect to login page
            return render_template('password_reset_successful.html')
        
        else:
            flash('Re-entered password does not match the password')
            return render_template('reset_password.html')

    else:
        return redirect('/404')


# Dashboard accessible if logged in
@app.route('/dashboard/')
def dashboard():
    if check_logged_in():
        username = session.get('username')
        return render_template('dashboard.html', username=username)
    else: # redirect to login page if user is not logged in
        return render_template('login_redirect.html')

# Logout
@app.route('/logout/')
def logout():
    if check_logged_in():
        # clean session tokens
        session.pop('logged_in', None)
        session.pop('username', None) 
        
        return redirect(url_for('frontpage'))
    else:
        return redirect('/404')


# Run the web application
if __name__ == '__main__': 
    app.run()
