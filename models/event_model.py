from dataclasses import dataclass, field
from typing import Optional
from dataclass_wizard import JSONWizard


@dataclass
class EventManager(JSONWizard):
    name: str
    date: str
    location: str
    capacity: int
    price: float
    tickets_booked: int


@dataclass
class Ticket(JSONWizard):
    event_id: str
    customer_name: str
    quantity: int
    total_price: float
   

