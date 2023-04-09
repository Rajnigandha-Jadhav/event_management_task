from bson import ObjectId
from datetime import date
from bson.json_util import loads, dumps
from database.database import db
from flask import Flask, request, jsonify
from logs.logger import setup_logger 
from models.event_model import EventManager, Ticket
from validations.validation import EventSchema, TicketSchema
event_schema = EventSchema()
ticket_schema = TicketSchema()
app = Flask(__name__)

# Create an event API

logger = setup_logger()

@app.route('/events', methods=['POST'])
def create_event():
    try:

        event_data = request.json
        if not event_data:
            return "Please provide some data", 400

        events = event_schema.load(event_data)
        event_Data = EventManager(name=events.name, date=events.date,
                                  location=events.location, capacity=events.capacity, price=events.price, tickets_booked=events.tickets_booked)
        event_info = vars(event_Data)
        db.events.insert_one(event_info)
        resp = jsonify({'message': 'Event created successfully'})
        resp.status_code = 201
        return resp

    except Exception as e:
        logger.error(str(e)) 
        return str(e), 500




# View events API
@app.route('/all-events', methods=['GET'])
def get_events():
    try:

        events = db.events.find()
        event_list = []

        for event in events:

            event_dict = {}
            event_dict['name'] = event['name']
            event_dict['date'] = event['date']
            event_dict['location'] = event['location']
            event_dict['capacity'] = event['capacity']
            event_dict['price'] = event['price']
            event_dict['tickets_booked'] = event['tickets_booked']

            event_list.append(event_dict)
        resp = jsonify(event_list)
        resp.status_code = 200
        return resp
    except Exception as e:
        logger.error(str(e)) 
        return str(e), 500


# Book ticket API
@app.route('/book-ticket', methods=['POST'])
def book_ticket():
    try:
        # Get request data
        data = request.get_json()

        # Validate request data
        booking = ticket_schema.load(data)
        event_id = booking.event_id
     

        customer = db.tickets.find_one(
            {'customer_name': booking.customer_name, 'event_id': booking.event_id})
        if customer:
            return jsonify({'error': 'Customer has already booked a ticket'}), 400

        # Check if event exists
        event = db.events.find_one({'_id': ObjectId(event_id)})
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        if event["capacity"] == event["tickets_booked"]:
            return jsonify({'error': 'All tickets are sold out'}), 404

        # Check if there are enough tickets available
        if booking.quantity > event["capacity"] - event["tickets_booked"]:
            return jsonify({'error': 'Not enough tickets available'}), 400

        # Update event tickets booked
        db.events.update_one({'_id': ObjectId(event_id)}, {
                             '$inc': {'tickets_booked': booking.quantity}})
        print(booking.quantity)
        # Create booking record
        booking_info = {
            'event_id': event_id,
            'customer_name': booking.customer_name,
            'quantity': booking.quantity,
            'total_price': booking.total_price
        }

        # Add booking record to database
        db.tickets.insert_one(booking_info)

        return jsonify({'success': True}), 201

    except Exception as e:
        logger.error(str(e)) 
        return str(e), 500

# View ticket API


@app.route('/all-tickets', methods=['GET'])
def get_tickets():
    try:
        

        tickets = db.tickets.find()
        ticket_list = []

        for ticket in tickets:
            eventDetails = db.events.find_one({"_id":ObjectId(ticket["event_id"])})
            eventDetails["_id"] = str(eventDetails["_id"])
        

            ticket_dict = {}
            ticket_dict['event_id'] = ticket['event_id']
            ticket_dict['customer_name'] = ticket['customer_name']
            ticket_dict['quantity'] = ticket['quantity']
            ticket_dict['total_price'] = ticket['total_price']
            ticket_dict['eventsData'] = eventDetails

            ticket_list.append(ticket_dict)
        resp = jsonify(ticket_list)
        resp.status_code = 200
        return resp
    except Exception as e:
        logger.error(str(e)) 
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)
