from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql as MySQLdb

# connect to database
db = MySQLdb.connect(host=input('Enter MySQL host: '),
                     user=input('Enter username: '),
                     passwd=input('Enter password: '),
                     db=input('Enter database name: '))
table = input('input table name: ')
cur = db.cursor()  # create cursor on mysqldb

# create the flask application
app = Flask(__name__)  # assign webpage to 'app'
app.secret_key = input('Enter secret key: ')  # secret key for session


# render HTML templates
@app.route('/')  # first page available on the site
def frontpage():
    return render_template('index.html') # render HTML on the page

@app.route('/home/')  # /home redirects to front page
def home():
    return redirect(url_for('frontpage'))

# login page
@app.route('/login/', methods=['POST', 'GET'])  
def login():

    if request.method == 'POST':
        
        # get form data
        username = request.form['username']
        password = request.form['password']
        
        # remove trailing whitespace from the credentials
        username = username.replace(" ", "")

        # check if login credentials exist
        if cur.execute("SELECT * FROM %s WHERE usernames = %s AND passwords = %s", (table, username, password)) == True:
            return render_template('login_successful.html') # render loading screen 
        else:
            flash('ERROR: Login unsuccessful. Username or password incorrect')

    return render_template('login.html')
    
# sign-up page
@app.route('/signup/', methods=['POST', 'GET'])  
def signup():
    if request.method == 'POST':
        
        # get form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # remove trailing whitespace from the credentials
        password = password.replace(" ", "") 
        username = username.replace(" ", "")
        email = email.replace(" ", "") 

        # check if username exists
        cur.execute("SELECT * FROM %s WHERE usernames = %s", (table, username))
        user_check = cur.fetchone()
        # check if email exists
        cur.execute("SELECT * FROM %s WHERE emails = %s", (table, email))
        email_check = cur.fetchone()

        if user_check:
            # if the username already exists
            flash('ERROR: Sign up unsuccessful. Username already exists')
            return render_template('signup.html')
        elif email_check:
            # if the email already exists
            flash('ERROR: Sign up unsuccessful. Email already exists')
            return render_template('signup.html')
        else:
            # insert data into database
            cur.execute("INSERT INTO %s (usernames, passwords, emails) VALUES (%s,%s,%s)",(table, username, password, email))
            db.commit()
            return render_template('signup_successful.html') # redirect to loading screen
            
    # render sign-up form
    return render_template('signup.html')


# run the web application
if __name__ == '__main__': 
    app.run()
