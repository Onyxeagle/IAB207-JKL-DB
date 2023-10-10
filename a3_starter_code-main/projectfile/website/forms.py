from flask_wtf import FlaskForm 
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, SelectField, DecimalField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed

class CreateEditForm(FlaskForm):
    eventName = StringField('Event Name', validators=[InputRequired()])
    startDate = DateField('Start Date', validators=[InputRequired()])
    endDate = DateField('End Date', validators=[InputRequired()])
    eventLocation = StringField('Event Location', validators=[InputRequired()])
    eventGenres = SelectField('Event Genre', choices=['Select Genre','Electronic', 'Classical', 'Rock', 'Metal', 'Pop'], validators=[InputRequired()])
    eventDescription = TextAreaField('Event Description', validators=[InputRequired()])
    numTickets = DecimalField('Number ofTickets', validators=[InputRequired()])
    costTickets = DecimalField('Ticket Price ($AUD)', validators=[InputRequired()])
    eventImage = FileField('Upload event image', validators=[InputRequired(), FileRequired()])
    submit = SubmitField('Create')

class DeleteForm(FlaskForm):
    PasswordField = StringField('Enter Password to delete', validators=[InputRequired()])
    delete = SubmitField('Delete')

class LogoutForm(FlaskForm):
    submit = SubmitField('Logout')

class LoginForm(FlaskForm):
    user_name = StringField('User Name', validators=[InputRequired('Enter user name')])
    password = StringField('Password', validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

class CreateAccountForm(FlaskForm):
    user_name = StringField('User Name', validators=[InputRequired('Enter user name')])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email address")])
    password = StringField('Password', validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

class HistoryForm(FlaskForm):
    submit = SubmitField('History')

class ValidEditForm(FlaskForm):
    submit = SubmitField('Editable Forms')

class TicketPurchase(FlaskForm):
    numTickets = DecimalField('Number of tickets to purchase', validators=[InputRequired()])
    submit = SubmitField('Purchase Ticket(s)')

class BookForm(FlaskForm):
    submit = SubmitField('Purchase Ticket (x remaining)')

class CommentForm(FlaskForm):
    submit = SubmitField('Comment')