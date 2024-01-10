from flask import request, session, flash, render_template, redirect, Blueprint
import pymysql as MySQLdb
from modules.SecurityChecks import hash_data
from config import db_hostname, db_username, db_password, db_database

AccountRecovery_blueprint = Blueprint('AccountRecovery', __name__)

# Account recovery
@AccountRecovery_blueprint.route('/forgot_password/',methods=['POST','GET'])
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
@AccountRecovery_blueprint.route('/reset_password/', methods=['POST'])
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
