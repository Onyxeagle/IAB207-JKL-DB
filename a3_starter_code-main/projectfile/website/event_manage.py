from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import CreateEditForm, DeleteForm, ValidEditForm
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from .models import Events
from . import db

eventbp = Blueprint('manage', __name__, url_prefix='/event_manage')

# creates a route for the event creation page and connects it to the database on submission
@eventbp.route('/create_event', methods=['GET','POST'])
#@login_required
def event_create():
    createForm = CreateEditForm()
    if createForm.validate_on_submit():
        flash('Successfully created your event! It has been posted for all to see.')
        db_file_path = check_upload_file(createForm)
        event = Events(name=createForm.eventName.data, description=createForm.eventDescription.data, genre=createForm.eventGenres.data, 
                       start_date=createForm.commenceDate.data, end_date=createForm.concludeDate.data, location=createForm.eventLocation.data, 
                       numTickets=createForm.numTickets.data, costTickets=createForm.costTickets.data, image=db_file_path, status='Open', )
        db.session.add(event)
        db.session.commit()
        print('Event created', 'Success')
        return redirect(url_for('manage.event_create'))
    return render_template('event_manage/create_event.html', form=createForm, heading='Create Event')

# creates the route for the event edit page
@eventbp.route('/edit_event', methods=['GET','POST'])
def event_edit():
    editForm = CreateEditForm()
    deleteForm = DeleteForm()
    return render_template('event_manage/edit_event.html', form=editForm, form2=deleteForm)

# a function that is used to direct the directory pathway for the image the user uploads
def check_upload_file(form):
    fp = form.eventImage.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
    db_upload_path = '/static/img/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path

# creates a route that will display the user's events that they have posted and are editable 
@eventbp.route('/editable_events', methods=['GET','POST'])
def editable_events():
    editableForm = ValidEditForm()
    return render_template('event_manage/edit_display.html', form=editableForm)