from flask_wtf import FlaskForm 
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, DecimalField, DateTimeField, IntegerField, SearchField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed

ALLOWED_FILE = {'PNG', 'png', 'JPG', 'jpg', 'JPEG', 'jpeg'}

# create the form that is used to display the create and edit forms for events
class CreateEditForm(FlaskForm):
    eventName = StringField('Event Name', validators=[InputRequired()])
    commenceDate = DateTimeField('Start Date (Only accepts YYYY-MM-DD H:M format and 24hr time)', format='%Y-%m-%d %H:%M', validators=[InputRequired(message='Please enter a valid date')])
    concludeDate = DateTimeField('End Date (Only accepts YYYY-MM-DD H:M format and 24hr time)', format='%Y-%m-%d %H:%M', validators=[InputRequired(message='Please enter a valid date')])
    eventLocation = StringField('Event Location', validators=[InputRequired()])
    eventGenres = SelectField('Event Genre', choices=['Select Genre','Electronic', 'Classical', 'Rock', 'Metal', 'Pop'], validators=[InputRequired()])
    eventDescription = TextAreaField('Event Description', validators=[InputRequired()])
    numTickets = IntegerField('Number ofTickets', validators=[InputRequired()])
    costTickets = DecimalField('Ticket Price ($AUD)', validators=[InputRequired()])
    eventImage = FileField('Upload event image', validators=[FileRequired(), FileAllowed(ALLOWED_FILE, message='supports jpg and png only')])
    submit = SubmitField('Create')

# create the form used to delete an event or delist it
# this won't actually delete the event record but will change it's status and prevent ticket purchase
class DeleteForm(FlaskForm):
    delete = SubmitField('Delete')

# a simple form for the user to log out
# this can be changed to be a button on index
class LogoutForm(FlaskForm):
    submit = SubmitField('Logout')

# this creates the login form that the user will pass data to so they can access their account
class LoginForm(FlaskForm):
    user_name = StringField('User Name', validators=[InputRequired('Enter user name')])
    password = PasswordField('Password', validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# the form used to create an account which takes parameters to differentiate users
class CreateAccountForm(FlaskForm):
    user_name = StringField('User Name', validators=[InputRequired('Enter user name')])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email address")])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

# to be done
# this form will be used to display the events a user is part of 
class HistoryForm(FlaskForm):
    submit = SubmitField('History')

# to be done
# this will display all the forms that can be edited by the user
# an editable form is one that is not inactive or cancelled 
# inactive being it is passed the end date and cancelled being a deletion 
class ValidEditForm(FlaskForm):
    submit = SubmitField('Editable Forms')

# to be done
# this form will be used to allow users to purchase tickets
class TicketPurchase(FlaskForm):
    numTickets = IntegerField('Number of tickets to purchase', validators=[InputRequired()])
    submit = SubmitField('Purchase Ticket(s)')

# to be done
# this is to go on the event page and will lead to the ticket purchase page
class BookForm(FlaskForm):
    submit = SubmitField('Purchase Ticket(s)')
 
# to be done
# the comment form that will display on each event
class CommentForm(FlaskForm):
    comment = TextAreaField('Write a comment', [InputRequired()])
    submit = SubmitField("Post comment")