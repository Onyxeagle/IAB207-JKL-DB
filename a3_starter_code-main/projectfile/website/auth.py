from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash,check_password_hash
#from .models import User
from .forms import LoginForm, CreateAccountForm
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

#create a blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    print('In Login testing')
    login = LoginForm
    error = None
    if login.validate_on_submit == True:
        username = login.user_name.data
        password = login.password.data
        user = db.session.scalar(db.select(User).where(User.name == username)) #this is a query 
        if user is None:
            error = 'Incorrect credentials supplied'
        elif not check_password_hash(User.password_hash, password):
            error = 'Incorrect credentials supplied'
        if error is None:
            #everything is in order, login the user with Flask Login
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form = login, heading='Login')

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    print('register testing')
    #set up variables and form
    register = CreateAccountForm()
    if register.validate_on_submit == True:
        username = register.user_name.data
        init_password = register.password.data
        email = register.email_id.data
        #check if a user or email already exists
        user = db.session.scalar(db.select(User).where(User.name == username))
        email_test = db.session.scalar(db.select(User).where(User.emailid == email))
        if user or email_test: #this returns true when user and/or email is not None
            flash('Username or email already in use, please use another')
            return redirect(url_for('auth.register'))
        password_hash = generate_password_hash(init_password)
        new_user = User(name = username, password_hash = password_hash, emailid = email)
        db.session.add(new_user)
        db.session.commit()
        print('You are now registered')

        #login the registered user automatically
        #login_user(new_user)
        return redirect(url_for('auth.login'))
    else:
        return render_template('user.html', form=register, heading='Register')
    
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
