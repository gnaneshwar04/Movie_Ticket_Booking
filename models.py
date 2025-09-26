# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from database import Base

class Movie(Base):
    #... (no changes here)
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    duration_minutes = Column(Integer)

class Theater(Base):
    #... (no changes here)
    __tablename__ = "theaters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)

class Hall(Base):
    __tablename__ = "halls"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    # This creates the link to the 'theaters' table's 'id' column
    theater_id = Column(Integer, ForeignKey("theaters.id"))

class Show(Base):
    __tablename__ = "shows"
    id = Column(Integer, primary_key=True, index=True)
    show_time = Column(DateTime)
    price = Column(Float)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    hall_id = Column(Integer, ForeignKey("halls.id"))

class Seat(Base):
    __tablename__ = "seats"
    id = Column(Integer, primary_key=True, index=True)
    row = Column(String)
    number = Column(Integer)
    hall_id = Column(Integer, ForeignKey("halls.id"))

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    booking_time = Column(DateTime)
    show_id = Column(Integer, ForeignKey("shows.id"))

class BookedSeat(Base):
    __tablename__ = "booked_seats"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    seat_id = Column(Integer, ForeignKey("seats.id"))

