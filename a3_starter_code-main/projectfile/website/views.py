from flask import Blueprint, render_template, request, redirect, url_for
from .models import Events
from sqlalchemy import or_
from . import db

mainbp = Blueprint('main', __name__)

# the default route landing page that will display index.html
@mainbp.route('/')
def index():
    event_list = Events.query.all()
    return render_template('index.html', event_list = event_list)

# identifies the search route and the forms to be displayed
# has an if statement that will also account for user search inputs that will return events that contain what they enter into the text field
# if nothing has been found it returns to index making it look like nothing has happened 

#db.select(Events).where(Events.name.like(query) or db.select(Events).where(Events.description).like(query) or db.select(Events).where(Events.genre).like(query))

@mainbp.route('/search')
def search():
    if (request.args['search'] and request.args['search'] != ""):
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        event_list = db.session.scalars(db.select(Events).filter(
            or_(Events.name.like(query), Events.description.like(query), Events.genre.like(query))))
        print(event_list)
        return render_template('index.html', event_list = event_list) #event_list variable added for correct search functionality
    else:
        return redirect(url_for('main.index')) 