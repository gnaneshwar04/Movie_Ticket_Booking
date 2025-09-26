# crud.py
from sqlalchemy.orm import Session
from datetime import date
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import func
import models
import schemas

def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(title=movie.title, duration_minutes=movie.duration_minutes)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_theaters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Theater).offset(skip).limit(limit).all()

def create_theater(db: Session, theater: schemas.TheaterCreate):
    db_theater = models.Theater(**theater.model_dump())
    db.add(db_theater)
    db.commit()
    db.refresh(db_theater)
    return db_theater

def get_halls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Hall).offset(skip).limit(limit).all()

def create_theater_hall(db: Session, hall: schemas.HallCreate, theater_id: int):
    db_hall = models.Hall(**hall.model_dump(), theater_id=theater_id)
    db.add(db_hall)
    db.commit()
    db.refresh(db_hall)
    return db_hall

def get_shows(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Show).offset(skip).limit(limit).all()

def create_show(db: Session, show: schemas.ShowCreate):
    db_show = models.Show(**show.model_dump())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show

def create_hall_seats(db: Session, hall_id: int, layout: schemas.HallLayoutCreate):
    seats_to_create = []
    for row, num_seats in layout.rows.items():
        for seat_num in range(1, num_seats + 1):
            seat = models.Seat(row=row, number=seat_num, hall_id=hall_id)
            seats_to_create.append(seat)

    db.add_all(seats_to_create) # Efficiently add all seats at once
    db.commit()
    return {"message": f"Created {len(seats_to_create)} seats for hall {hall_id}"}

def get_seats_for_hall(db: Session, hall_id: int):
    return db.query(models.Seat).filter(models.Seat.hall_id == hall_id).all()

def create_booking(db: Session, booking: schemas.BookingCreate):
    show = db.query(models.Show).filter(models.Show.id == booking.show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    # Find which seats belong to this show's hall
    possible_seat_ids = db.query(models.Seat.id).filter(models.Seat.hall_id == show.hall_id).all()
    possible_seat_ids = {seat.id for seat in possible_seat_ids}

    # Validate that all requested seat_ids are valid for this hall
    for seat_id in booking.seat_ids:
        if seat_id not in possible_seat_ids:
            raise HTTPException(status_code=400, detail=f"Seat ID {seat_id} is not valid for this show's hall.")

    # Now check for conflicts
    booked_seats_query = db.query(models.BookedSeat)\
        .join(models.Booking)\
        .filter(models.Booking.show_id == booking.show_id)\
        .filter(models.BookedSeat.seat_id.in_(booking.seat_ids))
    
    existing_booking = db.query(models.BookedSeat).join(models.Booking).filter(models.Booking.show_id == booking.show_id).filter(models.BookedSeat.seat_id.in_(booking.seat_ids)).first()

    if existing_booking:
        # If we find any existing booking for the requested seats, raise an error.
        num_seats_requested = len(booking.seat_ids)
        
        # Find all other shows for the same movie
        alternative_shows = db.query(models.Show).filter(
            models.Show.movie_id == show.movie_id,
            models.Show.id != show.id
        ).all()

        suggestions = []
        for alt_show in alternative_shows:
            # Count total seats in the hall for the alternative show
            total_seats = db.query(models.Seat).filter(models.Seat.hall_id == alt_show.hall_id).count()
            
            # Count booked seats for the alternative show
            booked_seats = db.query(models.BookedSeat).join(models.Booking).filter(models.Booking.show_id == alt_show.id).count()
            
            available_seats = total_seats - booked_seats
            
            if available_seats >= num_seats_requested:
                suggestions.append({"show_id": alt_show.id, "show_time": alt_show.show_time.isoformat()})

        detail = {
            "message": "One or more selected seats are already booked.",
            "suggestions": suggestions
        }
        raise HTTPException(status_code=409, detail=detail)
        

    # If no conflicts, proceed with booking
    db_booking = models.Booking(show_id=booking.show_id, booking_time=datetime.utcnow())
    db.add(db_booking)
    db.flush() # Use flush to get the new booking ID before committing

    for seat_id in booking.seat_ids:
        db_booked_seat = models.BookedSeat(booking_id=db_booking.id, seat_id=seat_id)
        db.add(db_booked_seat)

    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_movie_analytics(db: Session, movie_id: int, start_date: date, end_date: date):
    query_result = db.query(
        func.count(models.BookedSeat.id).label("total_tickets"),
        func.sum(models.Show.price).label("total_gmv")
    ).join(models.Booking, models.BookedSeat.booking_id == models.Booking.id)\
     .join(models.Show, models.Booking.show_id == models.Show.id)\
     .filter(
        models.Show.movie_id == movie_id,
        func.date(models.Show.show_time) >= start_date,
        func.date(models.Show.show_time) <= end_date
    ).one()

    # Handle case with no results
    if query_result.total_tickets is None:
        return {"total_tickets": 0, "total_gmv": 0.0}

    return {
        "total_tickets": query_result.total_tickets,
        "total_gmv": query_result.total_gmv
    }
