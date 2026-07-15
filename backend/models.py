from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Time,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(6), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    state = Column(String(50), nullable=False)
    zone = Column(String(10), nullable=False)


class Train(Base):
    __tablename__ = "trains"

    id = Column(Integer, primary_key=True, index=True)
    train_number = Column(String(10), unique=True, nullable=False)
    train_name = Column(String(100), nullable=False)
    origin = Column(String(50), nullable=False)
    destination = Column(String(50), nullable=False)
    departure_time = Column(Time, nullable=False)
    arrival_time = Column(Time, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    running_days = Column(String(50), nullable=False)
    ac_seats = Column(Integer, nullable=False, default=50)
    sleeper_seats = Column(Integer, nullable=False, default=100)
    ac_fare = Column(Float, nullable=False)
    sleeper_fare = Column(Float, nullable=False)
    route_stations = Column(ARRAY(String), nullable=False, default=[])

    bookings = relationship("Booking", back_populates="train")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    pnr = Column(String(10), unique=True, nullable=False, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"), nullable=False)
    travel_date = Column(Date, nullable=False)
    travel_class = Column(String(10), nullable=False)
    total_fare = Column(Float, nullable=False)
    email = Column(String(100), nullable=False, index=True)
    phone = Column(String(15), nullable=False)
    status = Column(String(20), nullable=False, default="confirmed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    train = relationship("Train", back_populates="bookings")
    passengers = relationship(
        "Passenger", back_populates="booking", cascade="all, delete-orphan"
    )


class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(
        Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    seat_preference = Column(String(20), default="No Preference")

    booking = relationship("Booking", back_populates="passengers")
