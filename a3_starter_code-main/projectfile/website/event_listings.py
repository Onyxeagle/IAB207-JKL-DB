from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .forms import TicketPurchase, BookForm, CommentForm
from .models import Events, Comment
from . import db
import os
from werkzeug.utils import secure_filename

listingbp = Blueprint('listing', __name__, url_prefix='/event_listing')

# creates the route used for the user purchasing tickets
# the user will need to be logged in to view this page
@listingbp.route('/ticket_purchase', methods=['GET','POST'])
@login_required
def purchase_tickets():
    purchaseform = TicketPurchase()
    return render_template('event_listings/purchase_tickets.html', form=purchaseform)

# creates the route that will display events based on an id fetched from the sqlite database
@listingbp.route('/view_event/<id>', methods=['GET','POST'])
def event_details(id):
    event = db.session.scalar(db.select(Events).where(Events.id == id))
    bookform = BookForm()
    comment = CommentForm()
    return render_template('event_listings/event_details.html', form=bookform, form2=comment, event=event)

# This function takes the information passed into the comment form and stores it into the database
@listingbp.route('/<id>/comment', methods=['GET','POST'])
@login_required
def eventComments(id):
    commentForm = CommentForm()
    commented_event = db.session.scalar(db.select(Events).where(Events.id == id))
    if commentForm.validate_on_submit():
        comment_to_post = Comment(text=commentForm.comment.data, user_id=current_user.id, events_id=commented_event.id)
        db.session.add(comment_to_post)
        db.session.commit()
        print('Comment made')
    return redirect(url_for('listing.event_details', id=id))