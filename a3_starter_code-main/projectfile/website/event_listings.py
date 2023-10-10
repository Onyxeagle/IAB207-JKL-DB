from flask import Blueprint, render_template, request, redirect, url_for
from .forms import TicketPurchase, BookForm, CommentForm

listingbp = Blueprint('listing', __name__, url_prefix='/event_listing')

@listingbp.route('/ticket_purchase', methods=['GET','POST'])
def purchase_tickets():
    purchaseform = TicketPurchase()
    return render_template('event_listings/purchase_tickets.html', form=purchaseform)

@listingbp.route('/view_event', methods=['GET','POST'])
def event_details():
    bookform = BookForm()
    comment = CommentForm()
    return render_template('event_listings/event_details.html', form=bookform, form2=comment)