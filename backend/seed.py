"""Seed script: populates stations and trains from data sources."""
from database import SessionLocal, engine
from models import Base, Station, Train
from stations_data import STATIONS
from generate_trains import make_trains


def seed_all():
    # Drop and recreate all tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # ─── Seed Stations ────────────────────────────────────────────────────
    station_objects = [
        Station(code=s["code"], name=s["name"], state=s["state"], zone=s["zone"])
        for s in STATIONS
    ]
    db.add_all(station_objects)
    print(f"Seeded {len(station_objects)} stations.")

    # ─── Seed Trains ──────────────────────────────────────────────────────
    trains_data = make_trains()
    train_objects = [
        Train(
            train_number=t["train_number"],
            train_name=t["train_name"],
            origin=t["origin"],
            destination=t["destination"],
            departure_time=t["departure_time"],
            arrival_time=t["arrival_time"],
            duration_hours=t["duration_hours"],
            running_days=t["running_days"],
            ac_seats=t["ac_seats"],
            sleeper_seats=t["sleeper_seats"],
            ac_fare=t["ac_fare"],
            sleeper_fare=t["sleeper_fare"],
            route_stations=t["route_stations"],
        )
        for t in trains_data
    ]
    db.add_all(train_objects)
    print(f"Seeded {len(train_objects)} trains.")

    db.commit()
    db.close()
    print("Database seeding complete!")


if __name__ == "__main__":
    seed_all()
