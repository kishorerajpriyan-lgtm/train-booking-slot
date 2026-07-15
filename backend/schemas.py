from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


# ─── Station ──────────────────────────────────────────────────────────────────

class StationResponse(BaseModel):
    id: int
    code: str
    name: str
    state: str
    zone: str

    model_config = {"from_attributes": True}


# ─── Passenger ────────────────────────────────────────────────────────────────

class PassengerCreate(BaseModel):
    name: str
    age: int
    gender: str
    seat_preference: str = "No Preference"

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        allowed = {"Male", "Female", "Other"}
        if v not in allowed:
            raise ValueError(f"Gender must be one of {allowed}")
        return v

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 1 or v > 120:
            raise ValueError("Age must be between 1 and 120")
        return v


class PassengerResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    seat_preference: str

    model_config = {"from_attributes": True}


# ─── Train (needed before BookingResponse) ───────────────────────────────────

class TrainInfo(BaseModel):
    """Minimal train info embedded in booking responses."""
    id: int
    train_number: str
    train_name: str
    origin: str
    destination: str

    model_config = {"from_attributes": True}


# ─── Booking ──────────────────────────────────────────────────────────────────

class BookingCreate(BaseModel):
    train_id: int
    travel_date: date
    travel_class: str
    email: EmailStr
    phone: str
    passengers: list[PassengerCreate]

    @field_validator("travel_class")
    @classmethod
    def validate_class(cls, v: str) -> str:
        if v not in ("AC", "Sleeper"):
            raise ValueError("travel_class must be 'AC' or 'Sleeper'")
        return v

    @field_validator("passengers")
    @classmethod
    def validate_passengers(cls, v: list[PassengerCreate]) -> list[PassengerCreate]:
        if not v:
            raise ValueError("At least one passenger is required")
        if len(v) > 6:
            raise ValueError("Maximum 6 passengers allowed per booking")
        return v


class BookingResponse(BaseModel):
    id: int
    pnr: str
    train_id: int
    travel_date: date
    travel_class: str
    total_fare: float
    email: str
    phone: str
    status: str
    created_at: datetime
    train: Optional[TrainInfo] = None
    passengers: list[PassengerResponse] = []

    model_config = {"from_attributes": True}


# ─── Train ────────────────────────────────────────────────────────────────────

class TrainResponse(BaseModel):
    id: int
    train_number: str
    train_name: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    duration_hours: int
    running_days: str
    ac_seats: int
    sleeper_seats: int
    ac_fare: float
    sleeper_fare: float
    route_stations: list[str] = []
    available_ac_seats: Optional[int] = None
    available_sleeper_seats: Optional[int] = None

    model_config = {}

    @classmethod
    def from_orm_time(cls, train):
        """Manually build response, converting time fields to strings."""
        return cls(
            id=train.id,
            train_number=train.train_number,
            train_name=train.train_name,
            origin=train.origin,
            destination=train.destination,
            departure_time=train.departure_time.strftime("%H:%M") if train.departure_time else "",
            arrival_time=train.arrival_time.strftime("%H:%M") if train.arrival_time else "",
            duration_hours=train.duration_hours,
            running_days=train.running_days,
            ac_seats=train.ac_seats,
            sleeper_seats=train.sleeper_seats,
            ac_fare=train.ac_fare,
            sleeper_fare=train.sleeper_fare,
            route_stations=train.route_stations or [],
        )


class TrainSearchParams(BaseModel):
    origin: str
    destination: str
    date: date
