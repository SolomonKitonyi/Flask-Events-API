from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
db = SQLAlchemy()

class User(db.Model,SerializerMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String,nullable=False)
    email =db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    events = db.relationship('Event', back_populates='organiser')
    bookings = db.relationship('Booking', back_populates='user')
    reviews = db.relationship('Reviews', back_populates='user')

class Event(db.Model,SerializerMixin):
    serialize_rules =('-organiser',)
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    description = db.Column(db.String,nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    organiser = db.relationship('User', back_populates='events')
    bookings = db.relationship('Booking', back_populates='event')
    reviews = db.relationship('Reviews', back_populates='event')


class Booking(db.Model, SerializerMixin):
    serialize_rules =('-event.bookings', '-user')
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ticket_no = db.Column(db.Integer)
    event = db.relationship('Event', back_populates='bookings')
    user = db.relationship('User', back_populates='bookings')

class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='reviews')
    event = db.relationship('Event', back_populates='reviews')







    