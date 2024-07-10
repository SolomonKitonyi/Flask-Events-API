from flask import Blueprint 
from flask_jwt_extended import jwt_required, current_user
from models import db, Event, Booking
from flask_restful import Api, Resource, reqparse
from auth import allow
attendee_bp = Blueprint('attendee_bp',__name__, url_prefix='/attendee')

attendee_api = Api(attendee_bp)

booking_args = reqparse.RequestParser()
booking_args.add_argument('ticket_no',required=True)

class Events(Resource):

    @jwt_required()
    @allow('organiser','attendee')
    def get(self ):
        events = Event.query.all()
        events = [event.to_dict() for event in events]
        return events


class BookingById(Resource):

    @jwt_required()
    @allow('organiser','attendee')
    def post(self, event_id):
        data = booking_args.parse_args()
        new_booking = Booking(event_id = event_id, user_id = current_user.id, ticket_no=data.get('ticket_no'))
        db.session.add(new_booking)
        db.session.commit()
        return {"msg": "event booked Successfully"}
    
    @jwt_required()
    @allow('organiser','attendee')
    def get(self, event_id):
        booking = Booking.query.filter_by(user_id=current_user.id, event_id= event_id).first()
        return booking.to_dict()


class Bookings(Resource):
     @jwt_required() 
     @allow('organiser','attendee') 
     def get(self):
         bookings = Booking.query.filter_by(user_id= current_user.id).all()
         bookings = [booking.to_dict() for booking in bookings]
         return bookings
    


attendee_api.add_resource(Events, '/events')
attendee_api.add_resource(BookingById, '/events/<int:event_id>')
attendee_api.add_resource(Bookings,'/bookings')
