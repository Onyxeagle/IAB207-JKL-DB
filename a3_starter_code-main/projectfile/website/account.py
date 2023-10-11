from flask import Blueprint, render_template, request, redirect, url_for
from .forms import LoginForm, LogoutForm, CreateAccountForm, HistoryForm

accountbp = Blueprint('account', __name__, url_prefix='/account')

# create the route for the sign in page
@accountbp.route('/sign_in', methods=['GET','POST'])
def sign_in():
    login = LoginForm()
    return render_template('account/login.html', form=login)

# create the route for hte sign out page
@accountbp.route('/sign_out', methods=['GET','POST'])
def sign_out():
    logout = LogoutForm()
    return render_template('account/logout.html', form=logout)

# create the route for the account creation page
@accountbp.route('/create_account', methods=['GET','POST'])
def createAccount():
    create_account = CreateAccountForm()
    return render_template('account/create_account.html', form=create_account)

# create the route to the booking history page
@accountbp.route('/booking_history', methods=['GET','POST'])
def History():
    historyform = HistoryForm()
    return render_template('account/account_history.html', form=historyform)