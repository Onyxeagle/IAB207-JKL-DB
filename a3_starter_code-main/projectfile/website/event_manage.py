from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import CreateEditForm, DeleteForm, ValidEditForm
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from .models import Events
from . import db
from datetime import datetime


eventbp = Blueprint('manage', __name__, url_prefix='/event_manage')

# creates a route for the event creation page and connects it to the database on submission
@eventbp.route('/create_event', methods=['GET','POST'])
@login_required
def event_create():
    createForm = CreateEditForm()
    if (createForm.validate_on_submit() and valid_date(createForm.commenceDate.data, createForm.concludeDate.data))==True:
        flash('Successfully created your event! It has been posted for all to see.')
        db_file_path = check_upload_file(createForm)
        event = Events(name=createForm.eventName.data, description=createForm.eventDescription.data, genre=createForm.eventGenres.data, 
                       start_date=createForm.commenceDate.data, end_date=createForm.concludeDate.data, location=createForm.eventLocation.data, 
                       numTickets=createForm.numTickets.data, costTickets=createForm.costTickets.data, image=db_file_path, status='Open', event_poster=current_user.id)
        db.session.add(event)
        db.session.commit()
        print('Event created', 'Success')
        return redirect(url_for('manage.event_create'))
    return render_template('event_manage/create_event.html', form=createForm, heading='Create Event')

# creates the route for the event edit page
@eventbp.route('/<id>/edit_event', methods=['GET','POST'])
def event_edit(id):
    editForm = CreateEditForm()
    event = db.session.query(Events).filter(Events.id == id)
    if (editForm.validate_on_submit() and valid_date(editForm.commenceDate.data, editForm.concludeDate.data))==True:
        db_file_path = check_upload_file(editForm)
        # updates a row with the same event id as the one passed to the function
        db.session.query(Events).\
        filter(Events.id == id).\
        update({'name': editForm.eventName.data ,'start_date': editForm.commenceDate.data,'end_date': editForm.concludeDate.data,
                'description': editForm.eventDescription.data,'genre': editForm.eventGenres.data,'image': db_file_path, 
               'numTickets': editForm.numTickets.data,'costTickets': editForm.costTickets.data,'location': editForm.eventLocation.data,'status': 'Open'})
        db.session.commit()
        return redirect(url_for('listing.event_details', id=id))
    deleteForm = DeleteForm()
    # if the delete form is submitted it will then change the event status to cancelled
    if deleteForm.validate_on_submit():
        stats = "Cancelled"
        db.session.query(Events).\
        filter(Events.id == id).\
        update({'status': stats})
        db.session.commit()
        return redirect(url_for('listing.event_details', id=id))
    return render_template('event_manage/edit_event.html', form=editForm, form2=deleteForm, event=event)


# a function that is used to direct the directory pathway for the image the user uploads
def check_upload_file(form):
    fp = form.eventImage.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
    db_upload_path = '/static/img/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path

# a function that checks the validity of an entered date and returns a response based on what was entered
# checks if the start date is less than current date and if the end date is less than or equal to the start date
def valid_date(start_date, end_date):
    valid = False
    if start_date >= end_date:
        flash('Start date cannot be after end date', 'error') 
    elif start_date <= datetime.now():
        flash('Start date cannot be a date that has passed', 'error')
    else:
        valid = True
    return valid

# creates a route that will display the user's events that they have posted and are editable 
@eventbp.route('/editable_events', methods=['GET','POST'])
@login_required
def editable_events():
    id = current_user.id 
    # using a query the events that share the same poster ID as the current user will be added to a list called events which is passed to the template
    events = db.session.query(Events).filter(Events.event_poster == id)
    editableForm = ValidEditForm()
    return render_template('event_manage/edit_display.html', form=editableForm, events=events)