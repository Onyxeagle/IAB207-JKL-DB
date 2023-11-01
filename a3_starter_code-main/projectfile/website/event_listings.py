from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import TicketPurchase, BookForm, CommentForm, TicketPurchase
from .models import Events, Comment, Bookings
from . import db

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
    if (purchaseform.validate_on_submit() and ticket_check(id, purchaseform.numTickets.data))==True:
        totalCost = purchaseform.numTickets.data * purchase_event.costTickets
        puchase = Bookings(bought_tickets=purchaseform.numTickets.data, total_cost=totalCost, event_details=purchase_event.name, ticket_purchaser=current_user.id)
        db.session.add(puchase)
        db.session.commit()
        # gets the most recent record from the database filtering by ID 
        # most recent record will be the user's purchase
        real = db.session.query(Bookings).order_by(Bookings.id.desc()).first()
        flash(f'Purchase successful! Your transaction ID is: {real.id}')
        # decrements the tickets from the event database numTicket value
        decrement_tickets(purchase_event.id, purchaseform.numTickets.data)
        return redirect(url_for('listing.purchase_tickets', id=id))
    return render_template('event_listings/purchase_tickets.html', form=purchaseform, event=purchase_event)

# this function updates the number of purchasable tickets when a user makes a purchase
def decrement_tickets(id, purchasedTickets):
    purchase_event = db.session.scalar(db.select(Events).where(Events.id == id))
    tickets = purchase_event.numTickets
    new_tickets = purchase_event.numTickets - purchasedTickets
    # updates a row with the same event id as the one passed to the function
    db.session.query(Events).\
    filter(Events.id == id).\
    update({'numTickets': (tickets - purchasedTickets)})
    # if the purchase results in the number of tickets becoming zero then replace the status 
    if new_tickets == 0:
        db.session.query(Events).\
        filter(Events.id == id).\
        update({'status': 'Sold Out'})
    db.session.commit()
    
# function that checks the tickets being purchased against the available tickets and provides the appropriate response
def ticket_check(id, purchasedTickets):
    purchase_event = db.session.scalar(db.select(Events).where(Events.id == id))
    availableTickets = purchase_event.numTickets
    if purchasedTickets > availableTickets:
        flash('Cannot order more tickets than what is available')
        return False
    elif purchasedTickets <= 0:
        flash('Cannot purchase that number of tickets')
        return False
    else:
        return True