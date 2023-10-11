from flask import Blueprint, render_template

mainbp = Blueprint('main', __name__)

# the default route landing page that will display index.html
@mainbp.route('/')
def index():
    return render_template('index.html')