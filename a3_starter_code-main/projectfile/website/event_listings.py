from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .forms import TicketPurchase, BookForm, CommentForm, TicketPurchase
from .models import Events, Comment, Bookings
from . import db
from sqlalchemy import update

listingbp = Blueprint('listing', __name__, url_prefix='/event_listing')

# creates the route that will display events based on an id fetched from the sqlite database
@listingbp.route('/view_event/<id>', methods=['GET','POST'])
def event_details(id):
    event = db.session.scalar(db.select(Events).where(Events.id == id))
    bookform = BookForm()
    if bookform.validate_on_submit():
        return (redirect(url_for('listing.purchase_tickets')))
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
    return redirect(url_for('listing.event_details', id=id))

# creates the route used for the user purchasing tickets
# the user will need to be logged in to view this page
@listingbp.route('<id>/ticket_purchase', methods=['GET','POST'])
@login_required
def purchase_tickets(id):
    purchaseform = TicketPurchase()
    purchase_event = db.session.scalar(db.select(Events).where(Events.id == id))
    if purchaseform.validate_on_submit():
        totalCost = purchaseform.numTickets.data * purchase_event.costTickets
        puchase = Bookings(bought_tickets=purchaseform.numTickets.data, total_cost=totalCost, event_details=purchase_event.id, ticket_purchaser=current_user.id)
        db.session.add(puchase)
        db.session.commit()
        decrement_tickets(id, purchaseform.numTickets.data)
        return redirect(url_for('listing.purchase_tickets', id=id))
    return render_template('event_listings/purchase_tickets.html', form=purchaseform, event=purchase_event)

# this function updates the number of purchasable tickets when a user makes a purchase
def decrement_tickets(id, purchasedTickets):
    purchase_event = db.session.scalar(db.select(Events).where(Events.id == id))
    tickets = purchase_event.numTickets
    print(tickets)
    db.session.query(Events).\
    filter(id == id).\
    update({'numTickets': (tickets - purchasedTickets)})
    db.session.commit()
