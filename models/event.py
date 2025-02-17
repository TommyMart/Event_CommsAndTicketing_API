# External Libraries
from marshmallow import fields,validate
from marshmallow.validate import Regexp, Length, And

# Imports from local files
from init import db, ma

# Table model class for the events table in the DB


class Event(db.Model):
    try:
        # Name of the table
        __tablename__ = "events"

        # Table Attributes
        # ID column - Integer data type and primary key of the "events" table
        id = db.Column(db.Integer, primary_key=True)
        # Title column - String data type
        title = db.Column(db.String)
        # Description column - String data type
        description = db.Column(db.String)
        # Date column - Date data type
        date = db.Column(db.Date)
        # Ticket price column - Float data type with a default value of 0.00
        ticket_price = db.Column(db.Float, default=0.00)

        # Foreign Keys
        # Event admin ID column - Foreign key referencing the ID attribute
        # from the users table
        # Cannot be null because an event must be associated with a user
        event_admin_id = db.Column(
            db.Integer, db.ForeignKey("users.id"), nullable=False)

        # Relationships
        # Link to the User model - An event is associated with a single user
        user = db.relationship("User", back_populates="events")
        # Link to the Attending model - An event can have multiple
        # attending records
        attending = db.relationship(
            "Attending", back_populates="event", cascade="all, delete")
        # Link to the Invoice model - An event can have multiple invoices
        invoice = db.relationship(
            "Invoice", back_populates="event", cascade="all, delete")
    except Exception as e:
        # Handle unexpected errors
        print(str(e)), 500

# Schema instance from Marshmallow - Convert DB objects to
# Python objects and vice versa


class EventSchema(ma.Schema):
    try:
        # Relationships
        # An event is associated with a single user (nested object)
        user = fields.Nested("UserSchema", only=["name", "email"])
        # An event can have multiple attending records (list)
        attending = fields.List(fields.Nested("AttendingSchema", only=[
                                "event_id", "seat_section", "total_tickets", "user"]))
        # An event can have multiple invoices (list)
        invoice = fields.List(fields.Nested(
            "InvoiceSchema", only=["total_cost"]))

        # Validation
        # Title column - String data type and cannot be null
        title = fields.String(required=True, validate=And(
            # Title must be at least 3 characters long
            Length(min=3, max=50,
                   error="Title must be between 3 and 50 characters long"),
            # Title must contain alphanumeric characters only
            Regexp("^[A-Za-z0-9 ]+$",
                   error="Title must contain alphanumeric characters only")
        ))
        # Description column - String data type and cannot be null
        description = fields.String(validate=And(
            # Description must be less than 400 characters long
            Length(
                max=400, error="Event description must be less than 400 characters long"),
            # Description must contain alphanumeric characters only
            Regexp("^[A-Za-z0-9 ]+$",
                   error="Event description must contain alphanumeric characters only")
        ))
        # Date column - Date data value
        date = fields.String(validate=  # Date must be written as dd/mm/yyyy only
                             Regexp(
                                 r"^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$",
                                 error="Date must be written as dd/mm/yyyy only")
                             )
        # Ticket price column - Float data type
        ticket_price = fields.Float(validate=validate.Range(min=0.0,
                                                            error="Ticket price must be a positive number"))

        # Meta class to define the fields to be included in the schema
        class Meta:
            # Fields to be included in the schema
            fields = ("id", "title", "description", "date", "ticket_price",
                      "event_admin_id", "user", "attending", "invoice")
    except Exception as e:
        # Handle unexpected errors
        print(str(e)), 500


# Schema for a single event object
event_schema = EventSchema()
# Schema for a list of event objects
events_schema = EventSchema(many=True)
