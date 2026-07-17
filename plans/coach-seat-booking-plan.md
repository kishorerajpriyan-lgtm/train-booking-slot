# Coach & Seat Number Booking System — Implementation Plan

**Goal:** Add compartment/coach-based seat allocation with individual seat numbers for booking.

---

## 1. Coach & Seat Model

### Database Changes

#### New Table: `coaches`
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | Coach ID |
| train_id | INTEGER FK | Which train |
| coach_code | VARCHAR(5) | e.g., "S1", "S2", "A1", "A2" |
| coach_type | VARCHAR(10) | "Sleeper" or "AC" |
| total_seats | INTEGER | Seats per coach (e.g., 72 for Sleeper, 54 for AC) |

#### New Table: `seats`
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | Seat ID |
| coach_id | INTEGER FK | Which coach |
| seat_number | VARCHAR(6) | e.g., "1", "2", ..., "72" or "1L", "1U", etc. |
| berth_type | VARCHAR(10) | "Lower", "Middle", "Upper", "Side-Lower", "Side-Upper" (Sleeper), "Lower", "Upper" (AC) |
| seat_type | VARCHAR(10) | "Window", "Aisle", "Middle" |

#### New Table: `booked_seats`
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | |
| booking_id | INTEGER FK | Which booking |
| passenger_id | INTEGER FK | Which passenger |
| seat_id | INTEGER FK | Which seat |
| travel_date | DATE | Date of travel |

### Modified Tables
- `trains`: Remove `ac_seats`/`sleeper_seats` columns — now computed from coaches
- `passengers`: Add `seat_id` FK (optional, assigned after booking)

---

## 2. Coach Generation

Trains get ~4-12 coaches based on type:
- **Rajdhani/Shatabdi:** 8 AC + 2 Sleeper coaches
- **Superfast/Mail/Express:** 2-4 AC + 6-10 Sleeper coaches
- **Intercity:** 2 AC + 4 Sleeper coaches

### Sleeper Coach Layout (72 seats per coach):
```
Seats 1-8:   1L-8L   (Lower berth)
Seats 9-16:  9M-16M  (Middle berth)
Seats 17-24: 17U-24U (Upper berth)
Seats 25-32: 25SL-32SL (Side Lower)
Seats 33-40: 33SU-40SU (Side Upper)
...continues to 72...
```

### AC Coach Layout (54 seats per coach):
```
Seats 1-9:   1L-9L   (Lower berth)
Seats 10-18: 10U-18U (Upper berth)
...continues to 54...
```

---

## 3. API Changes

| Method | Endpoint | Change |
|--------|----------|--------|
| `GET` | `/api/trains/{id}/seats?date=` | **New** — Returns coach layout with available/booked seats |
| `POST` | `/api/bookings` | **Modified** — Accepts optional `seat_preferences` per passenger; auto-assigns best available seats |
| `GET` | `/api/bookings/{pnr}` | **Modified** — Returns assigned seat numbers |

---

## 4. Seat Allocation Logic

**Priority Order:**
1. If passenger requested a seat preference (Window/Aisle), try to match
2. Prefer lower berths for passengers age > 60
3. Fill one coach before opening the next
4. Try to keep a booking's passengers together

---

## 5. Frontend Changes

| Component | Change |
|-----------|--------|
| `TrainCard.jsx` | Show coach counts instead of raw seat numbers |
| `BookingPage.jsx` | Show available coaches and seat map (optional view) |
| `ConfirmationPage.jsx` | Display assigned coach + seat for each passenger |

---

## 6. Implementation Steps

| # | Step | Files |
|---|------|-------|
| 1 | Add Coach, Seat, BookedSeat models | [`models.py`](backend/models.py) |
| 2 | Add schemas for seats/coaches | [`schemas.py`](backend/schemas.py) |
| 3 | Update train generator for coaches | [`generate_trains.py`](backend/generate_trains.py) |
| 4 | Create seat allocation engine | [`seat_allocator.py`](backend/seat_allocator.py) |
| 5 | Update booking/create endpoint | [`main.py`](backend/main.py) |
| 6 | Add GET seats endpoint | [`main.py`](backend/main.py) |
| 7 | Update frontend components | [`BookingPage.jsx`](frontend/src/pages/BookingPage.jsx), [`ConfirmationPage.jsx`](frontend/src/pages/ConfirmationPage.jsx) |
| 8 | Reseed & verify | All |

---

Ready to implement?
