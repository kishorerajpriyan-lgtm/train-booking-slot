"""Seed script: populates stations, trains, coaches and seats."""
from database import SessionLocal, engine
from models import Base, Station, Train, Coach, Seat
from stations_data import STATIONS
from generate_trains import make_trains, generate_seats


def seed_all():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # ─── Stations ────────────────────────────────────────────────────────
    station_objects = [
        Station(code=s["code"], name=s["name"], state=s["state"], zone=s["zone"])
        for s in STATIONS
    ]
    db.add_all(station_objects)
    db.flush()
    print(f"Seeded {len(station_objects)} stations.")

    # ─── Trains + Coaches + Seats ────────────────────────────────────────
    trains_data = make_trains()
    train_count = 0
    coach_count = 0
    seat_count = 0

    for t in trains_data:
        train = Train(
            train_number=t["train_number"],
            train_name=t["train_name"],
            origin=t["origin"],
            destination=t["destination"],
            departure_time=t["departure_time"],
            arrival_time=t["arrival_time"],
            duration_hours=t["duration_hours"],
            running_days=t["running_days"],
            ac_fare=t["ac_fare"],
            sleeper_fare=t["sleeper_fare"],
            route_stations=t["route_stations"],
        )
        db.add(train)
        db.flush()
        train_count += 1

        for coach_code, coach_type, total_seats in t["coaches"]:
            coach = Coach(
                train_id=train.id,
                coach_code=coach_code,
                coach_type=coach_type,
                total_seats=total_seats,
            )
            db.add(coach)
            db.flush()
            coach_count += 1

            for seat_num, berth, seat_type in generate_seats(coach_code, coach_type, total_seats):
                seat = Seat(
                    coach_id=coach.id,
                    seat_number=seat_num,
                    berth_type=berth,
                    seat_type=seat_type,
                )
                db.add(seat)
                seat_count += 1

    db.commit()
    db.close()
    print(f"Seeded {train_count} trains, {coach_count} coaches, {seat_count} seats.")
    print("Database seeding complete!")


if __name__ == "__main__":
    seed_all()
