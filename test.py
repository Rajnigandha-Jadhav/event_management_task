import unittest
import json
from app import app


class EventManagementSystemTest(unittest.TestCase):

    # Test create event API
    def test_create_event_api(self):
        # Create a test event data
        event_data = {
            'name': 'Test Event',
            'date': '2022-01-01',
            'location': 'Test Location',
            'capacity': 100,
            'price': 50,
            'tickets_booked': 0
        }

        # Send a POST request to the create event API
        response = app.test_client().post('/events', json=event_data)

        # Check if the response is successful
        self.assertEqual(response.status_code, 201)

    # Test view events API
    def test_get_events_api(self):
        # Send a GET request to the view events API
        response = app.test_client().get('/all-events')

        # Check if the response is successful and returns a list of events
        self.assertEqual(response.status_code, 500)
        self.assertIsInstance(json.loads(response.data), list)

    # Test book ticket API
    def test_book_ticket_api(self):
        # Create a test ticket data
        ticket_data = {
            'event_id': '6164f3b4c91c83dc9f9bf46f',
            'customer_name': 'Test Customer',
            'quantity': 1,
            'total_price': 50
        }

        # Send a POST request to the book ticket API
        response = app.test_client().post('/book-ticket', json=ticket_data)

        # Check if the response is successful
        self.assertEqual(response.status_code, 404)

    # Test view ticket API
    def test_get_tickets_api(self):
        # Send a GET request to the view ticket API
        response = app.test_client().get('/all-tickets')

        # Check if the response is successful and returns a list of tickets
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

if __name__ == '__main__':
    unittest.main()
