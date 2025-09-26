# schemas.py
from pydantic import BaseModel
from datetime import datetime


# --- Movie Schemas (from before) ---
class MovieBase(BaseModel):
    title: str
    duration_minutes: int

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    class Config:
        from_attributes = True

# --- Theater Schemas ---
class TheaterBase(BaseModel):
    name: str
    location: str

class TheaterCreate(TheaterBase):
    pass

class Theater(TheaterBase):
    id: int
    class Config:
        from_attributes = True
# --- ADD THESE NEW SCHEMAS ---
class HallBase(BaseModel):
    name: str

class HallCreate(HallBase):
    pass # We will add the theater_id in the endpoint itself

class Hall(HallBase):
    id: int
    theater_id: int # Include theater_id in the response
    class Config:
        from_attributes = True

class ShowBase(BaseModel):
    show_time: datetime
    price: float

class ShowCreate(ShowBase):
    movie_id: int
    hall_id: int

class Show(ShowBase):
    id: int
    movie_id: int
    hall_id: int
    class Config:
        from_attributes = True

class HallLayoutCreate(BaseModel):
    rows: dict[str, int]

class SeatBase(BaseModel):
    row: str
    number: int

class Seat(SeatBase):
    id: int
    hall_id: int
    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    show_id: int
    seat_ids: list[int] # Expects a list of seat IDs, e.g., [1, 2, 3]

class BookedSeat(BaseModel):
    id: int
    booking_id: int
    seat_id: int
    class Config:
        from_attributes = True

class Booking(BaseModel):
    id: int
    booking_time: datetime
    show_id: int
    class Config:
        from_attributes = True

# This will be the format for our suggestions
class ShowSuggestion(BaseModel):
    show_id: int
    show_time: datetime