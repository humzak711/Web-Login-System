from flask import request, session, flash, render_template, redirect, Blueprint
import pymysql as MySQLdb
from modules.SecurityChecks import hash_data, generate_recovery_key, check_logged_in
from config import db_hostname, db_username, db_password, db_database

AccountCreation_blueprint = Blueprint('AccountCreation', __name__)

# Login page
@AccountCreation_blueprint.route('/login/', methods=['POST', 'GET']) 
def login():
    if request.method == 'POST':
        
        # retreive user inputs
        login_username = request.form['username']
        login_password = request.form['password']

        # format user inputs to match database
        login_username = login_username.strip()
        login_username = login_username.lower()
        hashed_password = hash_data(login_password)
        
        # Connect to database
        db = MySQLdb.connect(host=db_hostname,
                     user=db_username,
                     passwd=db_password,
                     db=db_database)
        cur = db.cursor()  # create cursor on mysqldb
        
        # check if login credentials already exist
        CredentialsExist = cur.execute("SELECT * FROM users WHERE usernames = %s AND passwords = %s", (login_username,hashed_password))
        cur.close()
        db.close()

        # if login credentials exist
        if CredentialsExist:
            if check_logged_in(): # log user out from previous session
                session.pop('logged_in', None)
                session.pop('username', None)
            session['logged_in'] = True
            session['username'] = login_username
            return render_template('login_successful.html')
        else:
            flash('ERROR: Login unsuccessful. Username or password incorrect')

    return render_template('login.html')
    
    

# Sign-up page
@AccountCreation_blueprint.route('/signup/', methods=['POST', 'GET'])  
def signup():
    if request.method == 'POST':

        # clean session data 
        session.pop('signup_username', None)
        session.pop('signup_password', None)
        session.pop('signup_recovery_key', None)

        # retreive user inputs
        signup_username = request.form['username']
        signup_password = request.form['password']
        signup_re_password = request.form['re_password']
        
        # format inputs to match database
        signup_username = signup_username.strip()
        signup_password = signup_password.strip()
        signup_re_password = signup_re_password.strip()
        signup_username = signup_username.lower()
        
        # server side validation
        if signup_password != signup_re_password:
            flash('Re-entered password does not match the password.')
            return render_template('signup.html')
        
        # Connect to database
        db = MySQLdb.connect(host=db_hostname,
                     user=db_username,
                     passwd=db_password,
                     db=db_database)
        cur = db.cursor()  # create cursor on mysqldb

        # check if username already in use
        cur.execute("SELECT * FROM users WHERE usernames = %s", (signup_username))
        UsernameExist = cur.fetchone()
        cur.close()
        db.close()
        if UsernameExist:
            flash('ERROR: Sign up unsuccessful. Username already in use')
            return render_template('signup.html')
        else:
            signup_recovery_key = generate_recovery_key() # generate recovery key
            session['signup_username'] = signup_username
            session['signup_password'] = signup_password
            session['signup_recovery_key'] = signup_recovery_key
            return render_template('recovery_key.html', recovery_key=signup_recovery_key)
            
    return render_template('signup.html')

# Verify if recovery key is correct
@AccountCreation_blueprint.route('/verify_recovery_key/', methods=['POST'])
def verify_recovery_key():
    if request.method == 'POST':
        
        # retreive user inputs from recovery_key page
        entered_recovery_key = request.form['entered_recovery_key']
        
        # remove whitespace from entered recovery key
        entered_recovery_key = entered_recovery_key.strip()

        # retreive user inputs from signup page
        signup_recovery_key = session.get('signup_recovery_key')
        signup_password = session.get('signup_password')
        signup_username = session.get('signup_username')
        
        # if user input is correct, store credentials in database
        if signup_recovery_key == entered_recovery_key:

            # hash credentials
            hashed_password = hash_data(signup_password)
            hashed_recovery_key = hash_data(signup_recovery_key)
            
            # Connect to database
            db = MySQLdb.connect(host=db_hostname,
                     user=db_username,
                     passwd=db_password,
                     db=db_database)
            cur = db.cursor()  # create cursor on mysqldb
            
            # store data in database
            cur.execute("INSERT INTO users (usernames, passwords, recovery_keys) VALUES (%s,%s,%s)", (signup_username, hashed_password, hashed_recovery_key))
            db.commit()
            cur.close()
            db.close()
  
            # clean session data 
            session.pop('signup_username', None)
            session.pop('signup_password', None)
            session.pop('signup_recovery_key', None)

            # redirect user to login page
            return render_template('signup_successful.html')
        else:
            flash('ERROR: Please paste the recovery key correctly.')
            return render_template('recovery_key.html', recovery_key=signup_recovery_key) 
    else:
        return redirect('/404')



# Account recovery
@AccountCreation_blueprint.route('/forgot_password/',methods=['POST','GET'])
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
        
        # Connect to database
        db = MySQLdb.connect(host=db_hostname,
                     user=db_username,
                     passwd=db_password,
                     db=db_database)
        cur = db.cursor()  # create cursor on mysqldb
        
        # check if credentials are valid
        cur.execute("SELECT * FROM users WHERE usernames = %s AND recovery_keys = %s", (username, hashed_recovery_key))
        check_credentials = cur.fetchone()
        cur.close()
        db.close()
        if check_credentials:

            # pass username and hashed key to /reset_password
            session['Key_AccountRecovery'] = hashed_recovery_key
            session['Username_AccountRecovery'] = username
            return render_template('reset_password.html')
        else: 
            flash('Error: Username or recovery key incorrect')
            return render_template('forgot_password.html')
        
    return render_template('forgot_password.html') 

# Reset password 
@AccountCreation_blueprint.route('/reset_password/', methods=['POST'])
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
            
            # Connect to database
            db = MySQLdb.connect(host=db_hostname,
                    user=db_username,
                    passwd=db_password,
                    db=db_database)
            cur = db.cursor()  # create cursor on mysqldb
        
            # update database
            cur.execute("UPDATE users SET passwords = %s WHERE usernames = %s AND recovery_keys = %s", (hashed_new_password, username, hashed_recovery_key))
            db.commit()
            cur.close()
            db.close()

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
