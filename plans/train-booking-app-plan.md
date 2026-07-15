# Train Ticket Booking App — Implementation Plan

**Tech Stack:** React + Vite (Frontend) + Python/FastAPI (Backend) + PostgreSQL  
**Auth:** None (open access)  
**Scope:** Simple — search trains, book tickets, view/cancel bookings

---

## 1. Project Structure

```
Agentic AI/
├── backend/
│   ├── main.py                 # FastAPI app entry point, routes
│   ├── models.py               # SQLAlchemy ORM models
│   ├── database.py             # PostgreSQL connection & session
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── seed.py                 # Seed script to populate sample trains
│   ├── requirements.txt        # Python dependencies
│   └── alembic/                # (optional) DB migrations folder
│       └── versions/
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx             # Root component with routing
│   │   ├── App.css             # Global styles
│   │   ├── main.jsx            # Vite entry point
│   │   ├── api.js              # Axios API helper (base URL + fetch wrappers)
│   │   ├── components/
│   │   │   ├── Navbar.jsx      # Top navigation bar
│   │   │   ├── SearchForm.jsx  # Origin, Destination, Date, Class picker
│   │   │   ├── TrainCard.jsx   # Single train result card
│   │   │   ├── PassengerForm.jsx # Name, Age, Gender, Seat preference
│   │   │   └── BookingCard.jsx # Booking summary card (for My Bookings)
│   │   └── pages/
│   │       ├── HomePage.jsx    # Landing + search form
│   │       ├── SearchResultsPage.jsx  # List of matching trains
│   │       ├── BookingPage.jsx # Passenger details + confirm booking
│   │       ├── ConfirmationPage.jsx   # Booking success + PNR
│   │       └── MyBookingsPage.jsx     # List all bookings (lookup by email)
│   ├── vite.config.js
│   └── package.json
│
└── plans/
    └── train-booking-app-plan.md  # This file
```

---

## 2. Architecture Diagram

```mermaid
flowchart TD
    subgraph Frontend["React + Vite Frontend - port 5173"]
        HP[HomePage]
        SR[SearchResultsPage]
        BP[BookingPage]
        CP[ConfirmationPage]
        MB[MyBookingsPage]
        API[api.js - Axios]
    end

    subgraph Backend["FastAPI Backend - port 8000"]
        ROUTES[FastAPI Routes]
        SCHEMAS[Pydantic Schemas]
        MODELS[SQLAlchemy Models]
    end

    subgraph DB["PostgreSQL Database"]
        TRAINS[(trains)]
        BOOKINGS[(bookings)]
        PASSENGERS[(passengers)]
    end

    HP -->|search trains| SR
    SR -->|select train| BP
    BP -->|submit booking| CP
    MB -->|lookup by PNR/email| CP

    API -->|REST calls| ROUTES
    ROUTES --> SCHEMAS
    SCHEMAS --> MODELS
    MODELS --> TRAINS
    MODELS --> BOOKINGS
    MODELS --> PASSENGERS
```

---

## 3. Database Schema (PostgreSQL)

### Table: `trains`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PK | Unique train ID |
| train_number | VARCHAR(10) | NOT NULL, UNIQUE | e.g. "12345" |
| train_name | VARCHAR(100) | NOT NULL | e.g. "Rajdhani Express" |
| origin | VARCHAR(50) | NOT NULL | Source station code |
| destination | VARCHAR(50) | NOT NULL | Destination station code |
| departure_time | TIME | NOT NULL | Departure time |
| arrival_time | TIME | NOT NULL | Arrival time |
| duration_hours | INTEGER | NOT NULL | Travel duration in hours |
| running_days | VARCHAR(50) | NOT NULL | Comma-separated: "Mon,Tue,Wed" |
| ac_seats | INTEGER | NOT NULL, DEFAULT 50 | Total AC class seats |
| sleeper_seats | INTEGER | NOT NULL, DEFAULT 100 | Total Sleeper class seats |
| ac_fare | NUMERIC(10,2) | NOT NULL | Fare for AC class |
| sleeper_fare | NUMERIC(10,2) | NOT NULL | Fare for Sleeper class |

### Table: `bookings`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PK | Booking ID |
| pnr | VARCHAR(10) | NOT NULL, UNIQUE | 10-char unique PNR (auto-generated) |
| train_id | INTEGER | FK → trains.id | Which train |
| travel_date | DATE | NOT NULL | Travel date |
| travel_class | VARCHAR(10) | NOT NULL | "AC" or "Sleeper" |
| total_fare | NUMERIC(10,2) | NOT NULL | Sum of all passenger fares |
| email | VARCHAR(100) | NOT NULL | Contact email (used for lookup) |
| phone | VARCHAR(15) | NOT NULL | Contact phone |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'confirmed' | "confirmed" or "cancelled" |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Timestamp |

### Table: `passengers`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PK | Passenger ID |
| booking_id | INTEGER | FK → bookings.id ON DELETE CASCADE | Parent booking |
| name | VARCHAR(100) | NOT NULL | Full name |
| age | INTEGER | NOT NULL | Age |
| gender | VARCHAR(10) | NOT NULL | "Male"/"Female"/"Other" |
| seat_preference | VARCHAR(20) | DEFAULT 'No Preference' | "Window"/"Aisle"/"No Preference" |

---

## 4. API Endpoints (FastAPI)

| Method | Endpoint | Purpose | Request Body / Params | Response |
|--------|----------|---------|----------------------|----------|
| `GET` | `/api/trains/search` | Search trains | `?origin=&destination=&date=` | List of matching trains with available seats |
| `GET` | `/api/trains/{id}` | Get single train details | — | Train object |
| `POST` | `/api/bookings` | Create new booking | `BookingCreate` schema | Booking with PNR |
| `GET` | `/api/bookings/pnr/{pnr}` | Get booking by PNR | — | Booking + passengers |
| `GET` | `/api/bookings/` | Get all bookings by email | `?email=` | List of bookings |
| `PUT` | `/api/bookings/{pnr}/cancel` | Cancel a booking | — | Updated booking with status "cancelled" |

### Pydantic Schemas (`schemas.py`)

```python
class PassengerSchema(BaseModel):
    name: str
    age: int
    gender: str
    seat_preference: str = "No Preference"

class BookingCreate(BaseModel):
    train_id: int
    travel_date: date
    travel_class: str
    email: EmailStr
    phone: str
    passengers: list[PassengerSchema]

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
    passengers: list[PassengerSchema]

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
    available_ac_seats: int | None = None
    available_sleeper_seats: int | None = None
```

---

## 5. Frontend Routes & Component Tree

```
App.jsx
├── Navbar.jsx (persistent)
├── <Routes>
│   ├── "/" → HomePage.jsx
│   │         └── SearchForm.jsx (origin, destination, date, class)
│   │
│   ├── "/search" → SearchResultsPage.jsx
│   │                └── TrainCard.jsx (xN, one per train)
│   │
│   ├── "/book/:trainId" → BookingPage.jsx
│   │                       ├── Train summary info
│   │                       ├── Contact form (email, phone)
│   │                       └── PassengerForm.jsx (xN, one per passenger)
│   │
│   ├── "/confirmation/:pnr" → ConfirmationPage.jsx
│   │                           └── Booking summary + passenger list
│   │
│   └── "/my-bookings" → MyBookingsPage.jsx
│                          ├── Email lookup input
│                          └── BookingCard.jsx (xN)
```

### Frontend State Management

- **No Redux/Context needed** — simple prop drilling and URL params is sufficient for this scope.
- Search params are passed via URL query strings (`/search?origin=DEL&destination=MUM&date=2026-07-20`).
- Booking flow uses React Router `useNavigate` with state or URL params.

---

## 6. User Flow (Step by Step)

```
1. User lands on HomePage
   -> Fills: Origin, Destination, Travel Date, Class (AC/Sleeper)
   -> Clicks "Search Trains"

2. Navigates to SearchResultsPage
   -> Sees list of trains with: name, number, timings, fare, available seats
   -> Clicks "Book Now" on a train

3. Navigates to BookingPage
   -> Sees train summary at top
   -> Fills contact info (email, phone)
   -> Adds 1-6 passengers (name, age, gender, seat preference)
   -> Sees total fare dynamically
   -> Clicks "Confirm Booking"

4. API creates booking -> returns PNR
   -> Navigates to ConfirmationPage
   -> Shows PNR, train details, all passengers, fare
   -> Option: "Book Another" or "View My Bookings"

5. MyBookingsPage
   -> User enters email -> sees all bookings
   -> Each booking shows: PNR, train, date, status, fare
   -> Can cancel a booking (status changes to "cancelled")
```

---

## 7. Seed Data (Sample Trains)

The [`seed.py`](backend/seed.py) script will insert sample trains:

| Train Number | Name | Origin | Destination | Depart | Arrive | AC Fare | Sleeper Fare |
|---|---|---|---|---|---|---|---|
| 12301 | Rajdhani Express | DEL | MUM | 16:00 | 08:00 | 2500.00 | 900.00 |
| 12302 | Rajdhani Express | MUM | DEL | 17:00 | 09:00 | 2500.00 | 900.00 |
| 12621 | Tamil Nadu Exp | MAS | DEL | 22:00 | 07:00 | 2200.00 | 800.00 |
| 12951 | Mumbai Central | DEL | BLR | 14:30 | 06:30 | 2800.00 | 1000.00 |
| 12259 | Duronto Express | HWH | DEL | 20:00 | 10:00 | 2000.00 | 750.00 |
| 16526 | Bangalore Exp | MAS | SBC | 06:00 | 12:00 | 1200.00 | 450.00 |
| 12839 | Howrah Mail | HWH | MAS | 07:00 | 15:00 | 1800.00 | 650.00 |

---

## 8. Implementation Order (Build Steps)

| Step | What | File(s) | Description |
|------|------|---------|-------------|
| 1 | Backend setup | [`requirements.txt`](backend/requirements.txt), [`database.py`](backend/database.py) | FastAPI, SQLAlchemy, asyncpg/psycopg2, DB connection to PostgreSQL |
| 2 | SQLAlchemy models | [`models.py`](backend/models.py) | ORM models for trains, bookings, passengers |
| 3 | Pydantic schemas | [`schemas.py`](backend/schemas.py) | Request/response validation schemas |
| 4 | Seed script | [`seed.py`](backend/seed.py) | Populate 7 sample trains |
| 5 | FastAPI routes | [`main.py`](backend/main.py) | All 6 REST endpoints with CORS |
| 6 | Frontend scaffold | Vite + React setup, [`api.js`](frontend/src/api.js), routing | Vite project, Axios config, React Router |
| 7 | Navbar + HomePage | [`Navbar.jsx`](frontend/src/components/Navbar.jsx), [`HomePage.jsx`](frontend/src/pages/HomePage.jsx), [`SearchForm.jsx`](frontend/src/components/SearchForm.jsx) | Landing page with search form |
| 8 | Search Results | [`SearchResultsPage.jsx`](frontend/src/pages/SearchResultsPage.jsx), [`TrainCard.jsx`](frontend/src/components/TrainCard.jsx) | Display train list with availability |
| 9 | Booking Page | [`BookingPage.jsx`](frontend/src/pages/BookingPage.jsx), [`PassengerForm.jsx`](frontend/src/components/PassengerForm.jsx) | Passenger details + contact + submit |
| 10 | Confirmation + My Bookings | [`ConfirmationPage.jsx`](frontend/src/pages/ConfirmationPage.jsx), [`MyBookingsPage.jsx`](frontend/src/pages/MyBookingsPage.jsx), [`BookingCard.jsx`](frontend/src/components/BookingCard.jsx) | Booking success + view/cancel |
| 11 | Styling | [`App.css`](frontend/src/App.css) | Polish UI, responsive design |

---

## 9. Key Design Decisions

1. **No authentication** — booking lookup is done by email (simple, no login needed).
2. **FastAPI** — modern async Python framework with automatic OpenAPI/Swagger docs at `/docs`.
3. **PostgreSQL** — robust relational DB; requires a local or remote PostgreSQL instance.
4. **PNR generation** — UUID-based 10-character alphanumeric, generated server-side.
5. **Seat availability** — calculated dynamically: `total_seats - COUNT(booked)` for that train/date/class. No individual seat allocation (simplified).
6. **CORS** — FastAPI CORSMiddleware enabled for dev (Vite on `:5173`, FastAPI on `:8000`).
7. **Vite proxy** — [`vite.config.js`](frontend/vite.config.js) proxies `/api` requests to `http://localhost:8000` during development.
8. **Travel date validation** — only allow booking for future dates; running_days check ensures train runs on the selected weekday.
9. **Cancellation** — simply sets status to "cancelled"; no refund logic for simplicity.

---

## 10. Dependencies

### Backend (`requirements.txt`)
```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.35
psycopg2-binary==2.9.9
pydantic[email]==2.9.0
python-dotenv==1.0.1
```

### Frontend (`package.json` key deps)
```
react, react-dom, react-router-dom, axios
```
(Created via `npm create vite@latest` — Vite 5.x with React template.)

---

## 11. PostgreSQL Setup Notes

The app expects a PostgreSQL database to be running. Configuration via environment variables or a [`.env`](backend/.env) file:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/train_booking
```

The [`database.py`](backend/database.py) will use `create_all()` to auto-create tables on startup if they don't exist. For production, Alembic migrations should be used.

---

**Ready for your review.** Please confirm if you'd like any changes before I switch to Code mode for implementation.
