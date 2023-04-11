from dataclasses import dataclass, field
from typing import Optional
from dataclass_wizard import JSONWizard,JSONSerializable
from pymongo import MongoClient

@dataclass
class EventManager(JSONWizard):
    name: str
    date: str
    location: str
    capacity: int
    price: float
    tickets_booked: int
def save(self):
        # connect to the database
    client = MongoClient("mongodb://localhost:27017")
    db = client["eventmanager"]
    collection = db["events"]


@dataclass
class Ticket(JSONWizard):
    event_id: str
    customer_name: str
    quantity: int
    total_price: float
   

