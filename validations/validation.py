from marshmallow import Schema, fields, post_load
from models.event_model import EventManager, Ticket

# Marshmallow schema


class EventSchema(Schema):
    name = fields.Str(required=True)
    date = fields.Str()
    location = fields.Str(required=True)
    capacity = fields.Int(required=True)
    price = fields.Float(required=True)
    tickets_booked = fields.Int(default=0, validate=lambda n: n == 0)

    @post_load
    def create_event(self, data, **kwargs):
        return EventManager(**data)


class TicketSchema(Schema):
    event_id = fields.Str(required=True)
    customer_name = fields.Str(required=True)
    quantity = fields.Int(required=True)
    total_price = fields.Float(required=True)

    @post_load
    def create_ticket(self, data, **kwargs):
        return Ticket(**data)


#  event_id: str
#     customer_name: str
#     quantity: int
#     total_price: float