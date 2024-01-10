from flask import Blueprint, render_template, session, redirect, url_for
from modules.SecurityChecks import check_logged_in  

Dashboard_blueprint = Blueprint('dashboard', __name__)

# Dashboard accessible if logged in
@Dashboard_blueprint.route('/dashboard/')
def dashboard():
    if check_logged_in():
        username = session.get('username')
        return render_template('dashboard.html', username=username)
    else: # redirect to login page if user is not logged in
        return render_template('login_redirect.html')
    
# Access dashboard through API    
@Dashboard_blueprint.route('/dashboard/<username>/')
def dashboardAPI(username:str) -> render_template:
    if check_logged_in():
        if username.lower() == session.get('username'):
            return render_template('dashboard.html', username=username)
        else:
            return redirect(url_for('dashboard')) 
        
    else: # redirect to login page if user is not logged in
        return render_template('login_redirect.html')
    
# Logout
@Dashboard_blueprint.route('/logout/')
def logout():
    if check_logged_in():
        # clean session tokens
        session.pop('logged_in', None)
        session.pop('username', None) 
        
        return redirect(url_for('Home.frontpage'))
    else:
        return redirect('/404')
