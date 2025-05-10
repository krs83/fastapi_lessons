from pydantic import BaseModel, ConfigDict, Field
from datetime import date


class BookingsAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class Bookings(BookingsAdd):
    id: int
    user_id: int
    price: int

    model_config = ConfigDict(from_attributes=True)

