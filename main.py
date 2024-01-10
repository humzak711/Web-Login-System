from flask import Flask
from blueprints.Home import Home_blueprint
from blueprints.AccountCreation import AccountCreation_blueprint
from blueprints.AccountRecovery import AccountRecovery_blueprint
from blueprints.Dashboard import Dashboard_blueprint

# Create the Flask application
app = Flask(__name__)  
app.secret_key = input("input apps secret key: ")

# Register blueprints
app.register_blueprint(Home_blueprint) # Front page
app.register_blueprint(AccountCreation_blueprint) # Signup/Login
app.register_blueprint(AccountRecovery_blueprint) # Password reset
app.register_blueprint(Dashboard_blueprint) # User dashboard

# Run the web application
if __name__ == '__main__': 
    app.run()
