from flask import Blueprint, render_template

Home_blueprint = Blueprint('Home', __name__)

# Home pages
@Home_blueprint.route('/home/')  
@Home_blueprint.route('/')  
def frontpage():
    return render_template('index.html')
