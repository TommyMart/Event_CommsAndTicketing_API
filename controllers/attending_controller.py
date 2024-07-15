from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.attending import Attending, attending_schema, attendings_schema
from models.event import Event

from init import db

attending_bp = Blueprint("attending", __name__, url_prefix="/<int:event_id>/attending")

# no need to fetch all attending all events, only fetch all attending a specific event
# we can get all attending event by fetching an event

# /<int:event_id>/attending - POST - attending an event
@attending_bp.route("/", methods=["POST"])
@jwt_required()
def attending_event(event_id):
    body_data = request.get_json()

    stmt = db.select(Event).filter_by(id=event_id)
    event = db.session.scalar(stmt)

    if event:
        attending = Attending(
            total_tickets = body_data.get("total_tickets"),
            seat_number = body_data.get("seat_number"),
            timestamp = datetime.now(),
            event = event,
            attending_id = get_jwt_identity()
        )

        db.session.add(attending)
        db.session.commit()
        return attending_schema.dump(attending), 201
    
    else:
        return {"error": f"Event with id '{event_id}' not found"}, 404
        


# /<int:event_id>/attending/<int:attending_id> - DELETE - only require
# the attending id because event id has been fetched in the url_prefix
@attending_bp.route("/<int:attending_id>", methods=["DELETE"])
@jwt_required()
def delete_attending(attending_id):
    stmt = db.session(Attending).filter_by(id=attending_id)
    attending = db.session.scalar(stmt)

    if attending:
        db.session.delete(attending)
        db.session.commit()
        return {"message": f"Attending event '{Event.title}' deleted"}

    else:
        return {"error": f"Attendee with id '{attending_id}' not found"}
    

# Update comment - /posts/post_id/comments/comment_id
@attending_bp.route("/<int:attending_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_attending(attending_id):
    body_data = request.get_json()
    stmt = db.session(Attending).filter_by(id=attending_id)
    attending = db.session.scalar(stmt)

    if attending:

        attending.total_tickets = body_data.get("total_tickets") or attending.total_tickets
        attending.seat_number = body_data.get("seat_number") or attending.seat_number
        attending.time_stamp = body_data.get("time_stamp") or attending.time_stamp
    
        db.session.commit()
        return attending_schema.dump(attending)
    
    else:
        return {"error": f"Attending with id '{attending_id}' not found"}