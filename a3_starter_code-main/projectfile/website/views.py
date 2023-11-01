from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Events
from sqlalchemy import or_, update
from datetime import datetime
from . import db
mainbp = Blueprint('main', __name__)

# the default route landing page that will display index.html
@mainbp.route('/')
def index():
    init_event_list = Events.query.all()
    # checks if the event is active and if the end date has passed
    # if the end date has passed it will change the status to inactive
    # if the status is inactive or cancelled it will remove the event from the list that wil be turned into cards
    for event in init_event_list:
        ending_date = datetime.strptime(event.end_date, "%Y-%m-%d %H:%M:%S")
        if ending_date < datetime.now():
            db.session.query(Events).\
            filter(Events.id == event.id).\
            update({'status': "Inactive"})
            db.session.commit()
            init_event_list.remove(event)
        if event.status != "Open":
            init_event_list.remove(event)

    return render_template('index.html', event_list = init_event_list)

# identifies the search route and the forms to be displayed
# has an if statement that will also account for user search inputs that will return events that contain what they enter into the text field
# if nothing has been found it returns to index making it look like nothing has happened 

@mainbp.route('/search')
def search():
    if (request.args['search'] and request.args['search'] != ""):
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        event_list = db.session.scalars(db.select(Events).filter(
            or_(Events.name.like(query), Events.description.like(query), Events.genre.like(query))))
        init_event_list = event_list.all()
        for event in init_event_list:
            ending_date = datetime.strptime(event.end_date, "%Y-%m-%d %H:%M:%S")
            if ending_date < datetime.now():
                db.session.query(Events).\
                filter(Events.id == event.id).\
                update({'status': "Inactive"})
                db.session.commit()
                init_event_list.remove(event)
            if event.status != "Open":
                init_event_list.remove(event)

        return render_template('index.html', event_list = init_event_list) #event_list variable added for correct search functionality
    else:
        return redirect(url_for('main.index')) 