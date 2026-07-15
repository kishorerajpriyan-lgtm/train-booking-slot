"""FastAPI main application — Train Ticket Booking API."""
import uuid
import random
import string
from datetime import date, datetime

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db, init_db
from models import Train, Booking, Passenger, Station
from schemas import (
    BookingCreate,
    BookingResponse,
    TrainResponse,
    StationResponse,
)

app = FastAPI(title="Train Ticket Booking API", version="1.0.0")

# CORS — allow Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_pnr() -> str:
    """Generate a unique 10-character alphanumeric PNR."""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=10))


# ─── Startup ──────────────────────────────────────────────────────────────────

@app.on_event("startup")
def on_startup():
    init_db()


# ─── Station Routes ───────────────────────────────────────────────────────────

@app.get("/api/stations", response_model=list[StationResponse])
def get_all_stations(db: Session = Depends(get_db)):
    """Return all stations for frontend search/autocomplete."""
    return db.query(Station).order_by(Station.name).all()


# ─── Train Routes ─────────────────────────────────────────────────────────────

@app.get("/api/trains/search", response_model=list[TrainResponse])
def search_trains(
    origin: str = Query(..., min_length=1),
    destination: str = Query(..., min_length=1),
    travel_date: date = Query(...),
    db: Session = Depends(get_db),
):
    """Search trains by origin, destination, and travel date using route_stations."""
    origin_upper = origin.strip().upper()
    dest_upper = destination.strip().upper()

    # Determine day of week for running_days check
    day_name = travel_date.strftime("%a")  # "Mon", "Tue", etc.

    # Use PostgreSQL ARRAY containment: route_stations contains both origin AND destination
    # and origin appears before destination (simplified: just containment, order handled by route)
    trains = (
        db.query(Train)
        .filter(
            Train.route_stations.any(origin_upper),
            Train.route_stations.any(dest_upper),
            Train.running_days.contains(day_name),
        )
        .all()
    )

    result = []
    for train in trains:
        # Calculate available seats
        booked_ac = (
            db.query(func.count(Booking.id))
            .filter(
                Booking.train_id == train.id,
                Booking.travel_date == travel_date,
                Booking.travel_class == "AC",
                Booking.status == "confirmed",
            )
            .scalar()
            or 0
        )
        booked_sleeper = (
            db.query(func.count(Booking.id))
            .filter(
                Booking.train_id == train.id,
                Booking.travel_date == travel_date,
                Booking.travel_class == "Sleeper",
                Booking.status == "confirmed",
            )
            .scalar()
            or 0
        )

        train_data = TrainResponse.from_orm_time(train)
        train_data.available_ac_seats = max(0, train.ac_seats - booked_ac)
        train_data.available_sleeper_seats = max(0, train.sleeper_seats - booked_sleeper)
        result.append(train_data)

    return result  # returns empty list if no trains — no 404 error


@app.get("/api/trains/{train_id}", response_model=TrainResponse)
def get_train(train_id: int, db: Session = Depends(get_db)):
    """Get a single train by ID."""
    train = db.query(Train).filter(Train.id == train_id).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    return TrainResponse.from_orm_time(train)


# ─── Booking Routes ───────────────────────────────────────────────────────────

@app.post("/api/bookings", response_model=BookingResponse, status_code=201)
def create_booking(booking_data: BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking with passengers."""
    train = db.query(Train).filter(Train.id == booking_data.train_id).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    if booking_data.travel_date <= date.today():
        raise HTTPException(status_code=400, detail="Travel date must be in the future")

    day_name = booking_data.travel_date.strftime("%a")
    if day_name not in train.running_days:
        raise HTTPException(
            status_code=400,
            detail=f"Train {train.train_number} does not run on {day_name}",
        )

    num_passengers = len(booking_data.passengers)
    booked_count = (
        db.query(func.count(Booking.id))
        .filter(
            Booking.train_id == train.id,
            Booking.travel_date == booking_data.travel_date,
            Booking.travel_class == booking_data.travel_class,
            Booking.status == "confirmed",
        )
        .scalar()
        or 0
    )

    total_seats = (
        train.ac_seats if booking_data.travel_class == "AC" else train.sleeper_seats
    )
    available = total_seats - booked_count

    if num_passengers > available:
        raise HTTPException(
            status_code=400,
            detail=f"Only {available} seats available in {booking_data.travel_class} class",
        )

    fare_per_passenger = (
        train.ac_fare if booking_data.travel_class == "AC" else train.sleeper_fare
    )
    total_fare = fare_per_passenger * num_passengers

    pnr = generate_pnr()
    while db.query(Booking).filter(Booking.pnr == pnr).first():
        pnr = generate_pnr()

    booking = Booking(
        pnr=pnr,
        train_id=booking_data.train_id,
        travel_date=booking_data.travel_date,
        travel_class=booking_data.travel_class,
        total_fare=total_fare,
        email=booking_data.email,
        phone=booking_data.phone,
    )
    db.add(booking)
    db.flush()

    for p in booking_data.passengers:
        passenger = Passenger(
            booking_id=booking.id,
            name=p.name,
            age=p.age,
            gender=p.gender,
            seat_preference=p.seat_preference,
        )
        db.add(passenger)

    db.commit()
    db.refresh(booking)

    return BookingResponse.model_validate(booking)


@app.get("/api/bookings/pnr/{pnr}", response_model=BookingResponse)
def get_booking_by_pnr(pnr: str, db: Session = Depends(get_db)):
    """Get a booking by PNR number."""
    booking = db.query(Booking).filter(Booking.pnr == pnr.upper()).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return BookingResponse.model_validate(booking)


@app.get("/api/bookings/", response_model=list[BookingResponse])
def get_bookings_by_email(
    email: str = Query(..., min_length=1), db: Session = Depends(get_db)
):
    """Get all bookings for an email address."""
    bookings = (
        db.query(Booking)
        .filter(Booking.email.ilike(email.strip()))
        .order_by(Booking.created_at.desc())
        .all()
    )
    if not bookings:
        raise HTTPException(
            status_code=404, detail=f"No bookings found for email: {email}"
        )
    return [BookingResponse.model_validate(b) for b in bookings]


@app.put("/api/bookings/{pnr}/cancel", response_model=BookingResponse)
def cancel_booking(pnr: str, db: Session = Depends(get_db)):
    """Cancel a booking by PNR."""
    booking = db.query(Booking).filter(Booking.pnr == pnr.upper()).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking is already cancelled")

    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)

    return BookingResponse.model_validate(booking)


# ─── Health Check ─────────────────────────────────────────────────────────────

@app.get("/api/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
