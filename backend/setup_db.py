"""Setup script: creates the train_booking database and seeds it."""
import subprocess
import sys
import os

# First, try creating the database using Python + psycopg
try:
    import psycopg
    from psycopg import sql
    
    # Connect to postgres default database first
    conn = psycopg.connect(
        "dbname=postgres user=postgres password=kishore host=localhost port=5432"
    )
    conn.autocommit = True
    
    # Create database if not exists
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'train_booking'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("train_booking")))
            print("Database 'train_booking' created.")
        else:
            print("Database 'train_booking' already exists.")
    
    conn.close()
    print("Database setup complete.")
    
    # Now seed
    os.environ["DATABASE_URL"] = "postgresql://postgres:kishore@localhost:5432/train_booking"
    
    from database import init_db, SessionLocal
    from models import Train
    from datetime import time
    
    init_db()
    db = SessionLocal()
    
    if db.query(Train).count() > 0:
        print("Trains already seeded. Skipping.")
        db.close()
        sys.exit(0)
    
    trains = [
        Train(train_number="12301", train_name="Rajdhani Express", origin="DEL", destination="MUM",
              departure_time=time(16, 0), arrival_time=time(8, 0), duration_hours=16,
              running_days="Mon,Tue,Wed,Thu,Fri,Sat,Sun", ac_seats=50, sleeper_seats=100,
              ac_fare=2500.00, sleeper_fare=900.00),
        Train(train_number="12302", train_name="Rajdhani Express", origin="MUM", destination="DEL",
              departure_time=time(17, 0), arrival_time=time(9, 0), duration_hours=16,
              running_days="Mon,Tue,Wed,Thu,Fri,Sat,Sun", ac_seats=50, sleeper_seats=100,
              ac_fare=2500.00, sleeper_fare=900.00),
        Train(train_number="12621", train_name="Tamil Nadu Express", origin="MAS", destination="DEL",
              departure_time=time(22, 0), arrival_time=time(7, 0), duration_hours=33,
              running_days="Mon,Tue,Wed,Thu,Fri,Sat,Sun", ac_seats=50, sleeper_seats=120,
              ac_fare=2200.00, sleeper_fare=800.00),
        Train(train_number="12951", train_name="Mumbai Central", origin="DEL", destination="BLR",
              departure_time=time(14, 30), arrival_time=time(6, 30), duration_hours=16,
              running_days="Mon,Tue,Wed,Thu,Fri,Sat,Sun", ac_seats=60, sleeper_seats=110,
              ac_fare=2800.00, sleeper_fare=1000.00),
        Train(train_number="12259", train_name="Duronto Express", origin="HWH", destination="DEL",
              departure_time=time(20, 0), arrival_time=time(10, 0), duration_hours=14,
              running_days="Mon,Wed,Fri", ac_seats=40, sleeper_seats=80,
              ac_fare=2000.00, sleeper_fare=750.00),
        Train(train_number="16526", train_name="Bangalore Express", origin="MAS", destination="SBC",
              departure_time=time(6, 0), arrival_time=time(12, 0), duration_hours=6,
              running_days="Mon,Tue,Wed,Thu,Fri,Sat,Sun", ac_seats=30, sleeper_seats=60,
              ac_fare=1200.00, sleeper_fare=450.00),
        Train(train_number="12839", train_name="Howrah Mail", origin="HWH", destination="MAS",
              departure_time=time(7, 0), arrival_time=time(15, 0), duration_hours=8,
              running_days="Mon,Tue,Wed,Thu,Fri,Sat,Sun", ac_seats=40, sleeper_seats=90,
              ac_fare=1800.00, sleeper_fare=650.00),
    ]
    
    db.add_all(trains)
    db.commit()
    db.close()
    print(f"Seeded {len(trains)} trains successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
