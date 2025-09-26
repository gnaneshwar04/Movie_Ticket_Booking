# main.py
from fastapi import FastAPI, Depends
from datetime import date
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Movie Endpoints ---
@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies

@app.post("/movies/", response_model=schemas.Movie)
def create_movie_endpoint(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db=db, movie=movie)

# --- HALL ENDPOINTS ---
@app.get("/theaters/", response_model=list[schemas.Theater])
def read_theaters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    theaters = crud.get_theaters(db, skip=skip, limit=limit)
    return theaters

@app.post("/theaters/", response_model=schemas.Theater)
def create_theater_endpoint(theater: schemas.TheaterCreate, db: Session = Depends(get_db)):
    return crud.create_theater(db=db, theater=theater)

# --- Root Endpoint ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Algo Bharat Movie Booking API!"}

@app.get("/halls/", response_model=list[schemas.Hall])
def read_halls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    halls = crud.get_halls(db, skip=skip, limit=limit)
    return halls

# --- Hall Endpoints ---
# ...
@app.post("/theaters/{theater_id}/halls/", response_model=schemas.Hall)
def create_hall_for_theater(
    theater_id: int, hall: schemas.HallCreate, db: Session = Depends(get_db)
):
    return crud.create_theater_hall(db=db, hall=hall, theater_id=theater_id)

# --- SHOW ENDPOINTS ---
@app.get("/shows/", response_model=list[schemas.Show])
def read_shows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shows = crud.get_shows(db=db, skip=skip, limit=limit)
    return shows

@app.post("/shows/", response_model=schemas.Show)
def create_show_endpoint(show: schemas.ShowCreate, db: Session = Depends(get_db)):
    return crud.create_show(db=db, show=show)

@app.post("/halls/{hall_id}/layout/")
def create_hall_layout(hall_id: int, layout: schemas.HallLayoutCreate, db: Session = Depends(get_db)):
    return crud.create_hall_seats(db=db, hall_id=hall_id, layout=layout)

@app.get("/halls/{hall_id}/seats/", response_model=list[schemas.Seat])
def get_hall_seats(hall_id: int, db: Session = Depends(get_db)):
    return crud.get_seats_for_hall(db=db, hall_id=hall_id)

@app.post("/bookings/", response_model=schemas.Booking)
def create_booking_endpoint(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db=db, booking=booking)

# --- Root Endpoint ---

@app.get("/analytics/movies/{movie_id}/")
def get_analytics_for_movie(
    movie_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    return crud.get_movie_analytics(
        db=db, movie_id=movie_id, start_date=start_date, end_date=end_date
    )