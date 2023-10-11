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
    return render_template('event_manage/create_event.html', form=createForm)



# creates the route for the event edit page
@eventbp.route('/edit_event', methods=['GET','POST'])
def event_edit():
    editForm = CreateEditForm()
    deleteForm = DeleteForm()
    return render_template('event_manage/edit_event.html', form=editForm, form2=deleteForm)

# creates a route that will display the user's events that they have posted and are editable 
@eventbp.route('/editable_events', methods=['GET','POST'])
def editable_events():
    editableForm = ValidEditForm()
    return render_template('event_manage/edit_display.html', form=editableForm)