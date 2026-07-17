from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Time,
    ForeignKey,
    DateTime,
    UniqueConstraint,
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
    ac_fare = Column(Float, nullable=False)
    sleeper_fare = Column(Float, nullable=False)
    route_stations = Column(ARRAY(String), nullable=False, default=[])

    bookings = relationship("Booking", back_populates="train")
    coaches = relationship("Coach", back_populates="train", cascade="all, delete-orphan")


class Coach(Base):
    __tablename__ = "coaches"

    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id", ondelete="CASCADE"), nullable=False)
    coach_code = Column(String(5), nullable=False)  # "S1", "S2", "A1"
    coach_type = Column(String(10), nullable=False)  # "Sleeper" or "AC"
    total_seats = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint("train_id", "coach_code"),)

    train = relationship("Train", back_populates="coaches")
    seats = relationship("Seat", back_populates="coach", cascade="all, delete-orphan")


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey("coaches.id", ondelete="CASCADE"), nullable=False)
    seat_number = Column(String(6), nullable=False)  # "1", "2", "1L", "2U", etc.
    berth_type = Column(String(15), nullable=False)  # Lower, Middle, Upper, Side-Lower, Side-Upper
    seat_type = Column(String(10), nullable=False)  # Window, Aisle, Middle

    coach = relationship("Coach", back_populates="seats")
    booked_seats = relationship("BookedSeat", back_populates="seat", cascade="all, delete-orphan")


class BookedSeat(Base):
    __tablename__ = "booked_seats"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    passenger_id = Column(Integer, ForeignKey("passengers.id", ondelete="CASCADE"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id", ondelete="CASCADE"), nullable=False)
    travel_date = Column(Date, nullable=False)
    coach_code = Column(String(5), nullable=False)
    seat_number = Column(String(6), nullable=False)
    berth_type = Column(String(15), nullable=False)

    booking = relationship("Booking", back_populates="booked_seats")
    seat = relationship("Seat", back_populates="booked_seats")
    passenger = relationship("Passenger", back_populates="booked_seat")


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
    booked_seats = relationship(
        "BookedSeat", back_populates="booking", cascade="all, delete-orphan"
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
    booked_seat = relationship("BookedSeat", back_populates="passenger", uselist=False, cascade="all, delete-orphan")
