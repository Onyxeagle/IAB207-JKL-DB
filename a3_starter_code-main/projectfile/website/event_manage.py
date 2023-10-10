from flask import Blueprint, render_template, request, redirect, url_for
from .forms import CreateEditForm, DeleteForm, ValidEditForm

eventbp = Blueprint('manage', __name__, url_prefix='/event_manage')

@eventbp.route('/create_event', methods=['GET','POST'])
def event_create():
    createForm = CreateEditForm()
    return render_template('event_manage/create_event.html', form=createForm)

@eventbp.route('/edit_event', methods=['GET','POST'])
def event_edit():
    editForm = CreateEditForm()
    deleteForm = DeleteForm()
    return render_template('event_manage/edit_event.html', form=editForm, form2=deleteForm)

@eventbp.route('/editable_events', methods=['GET','POST'])
def editable_events():
    editableForm = ValidEditForm()
    return render_template('event_manage/edit_display.html', form=editableForm)