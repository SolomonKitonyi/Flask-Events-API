from flask import Blueprint 
from flask_restful import Api,Resource, reqparse 
from flask_jwt_extended import current_user, jwt_required
from models import db, Event
import datetime

organiser_bp = Blueprint('organiser_bp',__name__, url_prefix='/organiser')

organiser_api = Api(organiser_bp)
event_args = reqparse.RequestParser()
event_args.add_argument('name', type=str)
event_args.add_argument('description', type=str)
event_args.add_argument('price', type=float)
event_args.add_argument('date', type=str)


class Events(Resource):

    @jwt_required()
    def post(self):
        data = event_args.parse_args()
        event_date = datetime.datetime.now()
        new_event= Event(name = data.get('name'), description=data.get('description'), price=data.get('price'), date=event_date, user_id =current_user.id)
        db.session.add(new_event)
        db.session.commit()
        return {"msg":"event created Successfully"}
    
    @jwt_required()
    def get(self):
        events = Event.query.filter_by(user_id=current_user.id).all()
        events = [event.to_dict() for event in events]
        return events

organiser_api.add_resource(Events,'/events')

