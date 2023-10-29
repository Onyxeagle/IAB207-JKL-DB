from flask_login import UserMixin
from datetime import datetime
from . import db

# creates the database that will store user information and details
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # denote relationship to other tables
    comments = db.relationship('Comment', backref='user')
    posting = db.relationship('Events', backref='user')
    booker = db.relationship('Bookings', backref='user')

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

# creates a database that will store the events posted to the event
class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    genre = db.Column(db.String(20))
    location = db.Column(db.String(400))
    start_date = db.Column(db.String(30))
    end_date = db.Column(db.String(30))
    status = db.Column(db.String(20))
    image = db.Column(db.String(400))
    numTickets = db.Column(db.Integer)
    costTickets = db.Column(db.DECIMAL(2))
    # create relations to other databases
    comments = db.relationship('Comment', backref='events')
    bookedby = db.relationship('Bookings', backref='events')
    # foreign key
    event_poster = db.Column(db.Integer, db.ForeignKey('users.id'))

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

# creates a database that stores the bookings of events
class Bookings(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    bought_tickets = db.Column(db.Integer)
    total_cost = db.Column(db.DECIMAL(2))
    # foreign keys
    event_details = db.Column(db.Integer, db.ForeignKey('events.id'))
    ticket_purchaser = db.Column(db.Integer, db.ForeignKey('users.id'))

    # string print method
    def __repr__(self):
        return f"Name: {self.id}"

# creates a database that will store comments on specific evetns
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    events_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    
    # string print method
    def __repr__(self):
        return f"Name: {self.text}"