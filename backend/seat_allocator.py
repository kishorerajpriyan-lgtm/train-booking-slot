"""Seat allocation engine — assigns coach/seat numbers per passenger with preferences."""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Coach, Seat, BookedSeat


def get_available_seats(
    db: Session, train_id: int, travel_date: str, travel_class: str
) -> list[dict]:
    """Return all available seats for a train/date/class, ordered by preference."""
    seats_query = (
        db.query(Seat, Coach)
        .join(Coach, Seat.coach_id == Coach.id)
        .filter(
            Coach.train_id == train_id,
            Coach.coach_type == travel_class,
        )
        .outerjoin(
            BookedSeat,
            (BookedSeat.seat_id == Seat.id) & (BookedSeat.travel_date == travel_date),
        )
        .filter(BookedSeat.id.is_(None))
        .order_by(Coach.coach_code, Seat.seat_number)
        .all()
    )

    result = []
    for seat, coach in seats_query:
        result.append({
            "id": seat.id,
            "coach_code": coach.coach_code,
            "coach_id": coach.id,
            "seat_number": seat.seat_number,
            "berth_type": seat.berth_type,
            "seat_type": seat.seat_type,
        })
    return result


def allocate_seats(
    db: Session,
    train_id: int,
    travel_date: str,
    travel_class: str,
    passengers: list[dict],
) -> list[dict]:
    """
    Allocate seats for a list of passengers.
    Each passenger dict has: name, age, gender, seat_preference.
    Returns list of { passenger_index, seat_id, coach_code, seat_number, berth_type }.
    """
    available = get_available_seats(db, train_id, travel_date, travel_class)

    if len(passengers) > len(available):
        return None  # Not enough seats

    allocated = []
    used_seat_ids = set()

    # Sort passengers: seniors first (get lower berths), then others
    indexed_passengers = sorted(
        enumerate(passengers),
        key=lambda x: (
            0 if x[1].get("age", 0) >= 60 else 1,  # seniors first
            x[0],  # original order
        ),
    )

    for orig_idx, passenger in indexed_passengers:
        pref = passenger.get("seat_preference", "No Preference")
        is_senior = passenger.get("age", 0) >= 60
        best_seat = None

        # Try to find the best matching seat
        for seat in available:
            if seat["id"] in used_seat_ids:
                continue

            # Priority scoring
            score = 0

            # Seniors prefer Lower berths
            if is_senior:
                if seat["berth_type"] in ("Lower", "Side-Lower"):
                    score += 100
                elif seat["berth_type"] == "Middle":
                    score += 10
                elif seat["berth_type"] == "Upper":
                    score -= 50
                elif seat["berth_type"] == "Side-Upper":
                    score -= 30
            else:
                if seat["berth_type"] == "Lower":
                    score += 50
                elif seat["berth_type"] == "Side-Lower":
                    score += 40
                elif seat["berth_type"] == "Middle":
                    score += 20
                elif seat["berth_type"] == "Upper":
                    score += 0
                elif seat["berth_type"] == "Side-Upper":
                    score += 10

            # Window/Aisle preference
            if pref == "Window" and seat["seat_type"] == "Window":
                score += 30
            elif pref == "Aisle" and seat["seat_type"] == "Aisle":
                score += 30

            if best_seat is None or score > best_seat[1]:
                best_seat = (seat, score)

        if best_seat is None:
            # No seat found — shouldn't happen if we checked availability
            return None

        chosen_seat = best_seat[0]
        used_seat_ids.add(chosen_seat["id"])

        allocated.append({
            "passenger_index": orig_idx,
            "coach_code": chosen_seat["coach_code"],
            "coach_id": chosen_seat["coach_id"],
            "seat_id": chosen_seat["id"],
            "seat_number": chosen_seat["seat_number"],
            "berth_type": chosen_seat["berth_type"],
            "seat_type": chosen_seat["seat_type"],
        })

    # Sort back by original passenger index
    allocated.sort(key=lambda x: x["passenger_index"])
    return allocated


def get_coach_layout(
    db: Session, train_id: int, travel_date: str
) -> list[dict]:
    """Return full coach layout with seat availability for a train/date."""
    coaches = (
        db.query(Coach)
        .filter(Coach.train_id == train_id)
        .order_by(Coach.coach_code)
        .all()
    )

    layout = []
    for coach in coaches:
        seats = (
            db.query(Seat, BookedSeat.id.label("booked_id"))
            .outerjoin(
                BookedSeat,
                (BookedSeat.seat_id == Seat.id)
                & (BookedSeat.travel_date == travel_date),
            )
            .filter(Seat.coach_id == coach.id)
            .order_by(Seat.seat_number)
            .all()
        )

        seat_list = []
        for seat, booked_id in seats:
            seat_list.append({
                "seat_id": seat.id,
                "seat_number": seat.seat_number,
                "berth_type": seat.berth_type,
                "seat_type": seat.seat_type,
                "booked": booked_id is not None,
            })

        layout.append({
            "coach_id": coach.id,
            "coach_code": coach.coach_code,
            "coach_type": coach.coach_type,
            "total_seats": coach.total_seats,
            "available": sum(1 for s in seat_list if not s["booked"]),
            "seats": seat_list,
        })

    return layout
