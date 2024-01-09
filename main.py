from flask import Flask, render_template
from blueprints.Dashboard import Dashboard_blueprint
from blueprints.AccountCreation import AccountCreation_blueprint
from blueprints.Home import Home_blueprint

# Create the Flask application
app = Flask(__name__)  
app.secret_key = 'wo2aa38euhwugegwfr235ef36ewg827mawsvwgey3524eudnskjww'

# Register blueprints
app.register_blueprint(Home_blueprint) # Front page
app.register_blueprint(AccountCreation_blueprint) # Signup, Login, Account recovery
app.register_blueprint(Dashboard_blueprint) # User dashboard

# Run the web application
if __name__ == '__main__': 
    app.run()


# to do:
# bug hunt and pentest, find exploits and debug
    
# make a live chat with user chatbox rooms
 
# figure out how to implement sanitized CSRF tokens
# implement more sanitization and server side validation
# implement rate limitation