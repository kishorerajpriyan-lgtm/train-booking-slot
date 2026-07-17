import { useState, useEffect } from 'react';
import { useParams, useSearchParams, useNavigate } from 'react-router-dom';
import { getTrain, getTrainCoaches, createBooking } from '../api';

const COMPARTMENT_TYPES = [
  { key: 'Sleeper', label: 'Sleeper (SL)', icon: '🛏️' },
  { key: '3A', label: '3rd AC (3A)', icon: '❄️' },
  { key: '2A', label: '2nd AC (2A)', icon: '❄️❄️' },
  { key: '1A', label: '1st AC (1A)', icon: '❄️❄️❄️' },
];

function BookingPage() {
  const { trainId } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const travelDate = searchParams.get('date') || '';

  const [train, setTrain] = useState(null);
  const [coaches, setCoaches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // Step tracking
  const [selectedCompartment, setSelectedCompartment] = useState(null); // { key, coachCodes[] }
  const [selectedSeats, setSelectedSeats] = useState([]); // [{ coach_id, coach_code, seat_id, seat_number, berth_type }]
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [passengers, setPassengers] = useState([{ name: '', age: '', gender: '' }]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [trainRes, coachRes] = await Promise.all([
          getTrain(trainId),
          getTrainCoaches(trainId, travelDate),
        ]);
        setTrain(trainRes.data);
        setCoaches(coachRes.data);
      } catch (err) {
        setError('Failed to load train details.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [trainId, travelDate]);

  // Map coaches to compartment types
  const getCompartmentCoaches = (type) => {
    if (type === 'Sleeper') return coaches.filter((c) => c.coach_type === 'Sleeper');
    // 3A, 2A, 1A all use AC coaches — differentiated by coach code prefix
    return coaches.filter((c) => c.coach_type === 'AC');
  };

  const getCompartmentAvailability = (type) => {
    const compCoaches = getCompartmentCoaches(type);
    return compCoaches.reduce((sum, c) => sum + c.available, 0);
  };

  const getCompartmentFare = (type) => {
    if (!train) return 0;
    if (type === 'Sleeper') return train.sleeper_fare;
    if (type === '3A') return Math.round(train.ac_fare * 0.7);
    if (type === '2A') return train.ac_fare;
    if (type === '1A') return Math.round(train.ac_fare * 1.4);
    return 0;
  };

  const handleSelectCompartment = (comp) => {
    setSelectedCompartment(comp);
    setSelectedSeats([]);
  };

  const handleSelectSeat = (coach, seat) => {
    if (seat.booked) return;

    const alreadySelected = selectedSeats.find((s) => s.seat_id === seat.seat_id);
    if (alreadySelected) {
      // Deselect
      setSelectedSeats(selectedSeats.filter((s) => s.seat_id !== seat.seat_id));
    } else {
      if (selectedSeats.length >= 6) {
        alert('Maximum 6 seats per booking');
        return;
      }
      setSelectedSeats([
        ...selectedSeats,
        {
          coach_id: coach.coach_id,
          coach_code: coach.coach_code,
          seat_id: seat.seat_id,
          seat_number: seat.seat_number,
          berth_type: seat.berth_type,
        },
      ]);
    }
  };

  const handlePassengerChange = (index, field, value) => {
    const updated = [...passengers];
    updated[index] = { ...updated[index], [field]: value };
    setPassengers(updated);
  };

  const addPassengerRow = () => {
    if (passengers.length >= selectedSeats.length) {
      alert(`Add more seats first. Selected: ${selectedSeats.length}`);
      return;
    }
    setPassengers([...passengers, { name: '', age: '', gender: '' }]);
  };

  const removePassengerRow = (index) => {
    if (passengers.length <= 1) return;
    setPassengers(passengers.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (selectedSeats.length === 0) {
      alert('Please select at least one seat');
      return;
    }
    if (!email || !phone) {
      alert('Please fill contact details');
      return;
    }
    if (passengers.length !== selectedSeats.length) {
      alert('Number of passengers must match number of selected seats');
      return;
    }
    for (let i = 0; i < passengers.length; i++) {
      const p = passengers[i];
      if (!p.name || !p.age || !p.gender) {
        alert(`Please fill all details for Passenger ${i + 1}`);
        return;
      }
    }

    // Map to booking format
    const bookingData = {
      train_id: parseInt(trainId),
      travel_date: travelDate,
      travel_class: selectedCompartment.key === 'Sleeper' ? 'Sleeper' : 'AC',
      email,
      phone,
      passengers: passengers.map((p, i) => ({
        name: p.name,
        age: parseInt(p.age),
        gender: p.gender,
        seat_preference: 'No Preference',
      })),
    };

    try {
      setSubmitting(true);
      const res = await createBooking(bookingData);
      navigate(`/confirmation/${res.data.pnr}`);
    } catch (err) {
      alert(err.response?.data?.detail || 'Booking failed. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleBackToCompartments = () => {
    setSelectedCompartment(null);
    setSelectedSeats([]);
  };

  const totalFare = selectedSeats.length * getCompartmentFare(selectedCompartment?.key || '');

  if (loading) return <div className="loading">Loading train details...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!train) return null;

  // Get all available seats for selected compartment
  const compartmentCoaches = selectedCompartment ? getCompartmentCoaches(selectedCompartment.key) : [];

  return (
    <div className="booking-page">
      <h2>Complete Your Booking</h2>

      {/* Train Info */}
      <div className="booking-train-summary">
        <h3>{train.train_name}</h3>
        <p>
          <strong>{train.train_number}</strong> | {train.origin} → {train.destination} | {travelDate}
        </p>
      </div>

      {/* Step 1: Select Compartment */}
      {!selectedCompartment && (
        <div className="section-card">
          <h3>Select Compartment Type</h3>
          <div className="compartment-grid">
            {COMPARTMENT_TYPES.map((comp) => {
              const avail = getCompartmentAvailability(comp.key);
              const fare = getCompartmentFare(comp.key);
              return (
                <div
                  key={comp.key}
                  className={`compartment-card ${avail === 0 ? 'disabled' : ''}`}
                  onClick={() => avail > 0 && handleSelectCompartment(comp)}
                >
                  <div className="comp-icon">{comp.icon}</div>
                  <div className="comp-label">{comp.label}</div>
                  <div className="comp-info">
                    <span className="comp-avail">{avail} seats</span>
                    <span className="comp-fare">₹{fare.toLocaleString('en-IN')}/seat</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Step 2: Select Seats */}
      {selectedCompartment && (
        <>
          <div className="section-card">
            <div className="section-header">
              <button className="btn btn-secondary" onClick={handleBackToCompartments}>
                ← Back to Compartments
              </button>
              <h3>
                {selectedCompartment.label} — Select Seats
              </h3>
            </div>

            <div className="seat-grid-container">
              {compartmentCoaches.map((coach) => (
                <div key={coach.coach_id} className="coach-seat-section">
                  <h4 className="coach-title">{coach.coach_code} ({coach.available} available)</h4>
                  <div className="seat-grid">
                    {coach.seats.map((seat) => {
                      const isSelected = selectedSeats.some((s) => s.seat_id === seat.seat_id);
                      let seatClass = 'seat-cell';
                      if (seat.booked) seatClass += ' booked';
                      else if (isSelected) seatClass += ' selected';
                      else seatClass += ' available';

                      return (
                        <div
                          key={seat.seat_id}
                          className={seatClass}
                          title={`${coach.coach_code}/${seat.seat_number} — ${seat.berth_type} (${seat.seat_type})`}
                          onClick={() => handleSelectSeat(coach, seat)}
                        >
                          <span className="seat-num">{seat.seat_number}</span>
                          <span className="seat-berth">{seat.berth_type.charAt(0)}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Booking Summary */}
          {selectedSeats.length > 0 && (
            <div className="section-card booking-summary">
              <h3>📋 Booking Summary</h3>
              <div className="summary-grid">
                <div className="summary-item">
                  <span className="summary-label">Train Number</span>
                  <span className="summary-value">{train.train_number}</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Train Name</span>
                  <span className="summary-value">{train.train_name}</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Compartment</span>
                  <span className="summary-value">{selectedCompartment.label}</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Selected Seats</span>
                  <span className="summary-value">
                    {selectedSeats.map((s) => `${s.coach_code}/${s.seat_number}`).join(', ')}
                  </span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Fare/Seat</span>
                  <span className="summary-value">₹{getCompartmentFare(selectedCompartment.key).toLocaleString('en-IN')}</span>
                </div>
                <div className="summary-item">
                  <span className="summary-label">Total Fare</span>
                  <span className="summary-value total-fare">₹{totalFare.toLocaleString('en-IN')}</span>
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Passenger & Contact Details */}
          {selectedSeats.length > 0 && (
            <form onSubmit={handleSubmit}>
              <div className="section-card">
                <h3>Contact Details</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label>Email</label>
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="your@email.com" required />
                  </div>
                  <div className="form-group">
                    <label>Phone</label>
                    <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="9876543210" required />
                  </div>
                </div>
              </div>

              <div className="section-card">
                <h3>Passenger Details ({selectedSeats.length} seat(s))</h3>
                {passengers.map((p, i) => (
                  <div key={i} className="passenger-row">
                    <div className="passenger-seat-label">
                      Seat: <strong>{selectedSeats[i]?.coach_code}/{selectedSeats[i]?.seat_number}</strong> ({selectedSeats[i]?.berth_type})
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Name</label>
                        <input type="text" value={p.name} onChange={(e) => handlePassengerChange(i, 'name', e.target.value)} placeholder="Full name" required />
                      </div>
                      <div className="form-group">
                        <label>Age</label>
                        <input type="number" value={p.age} onChange={(e) => handlePassengerChange(i, 'age', e.target.value)} min="1" max="120" placeholder="Age" required />
                      </div>
                      <div className="form-group">
                        <label>Gender</label>
                        <select value={p.gender} onChange={(e) => handlePassengerChange(i, 'gender', e.target.value)} required>
                          <option value="">Select</option>
                          <option value="Male">Male</option>
                          <option value="Female">Female</option>
                          <option value="Other">Other</option>
                        </select>
                      </div>
                    </div>
                    {passengers.length > 1 && (
                      <button type="button" className="btn btn-danger-sm" onClick={() => removePassengerRow(i)}>✕ Remove</button>
                    )}
                  </div>
                ))}
                {passengers.length < selectedSeats.length && (
                  <button type="button" className="btn btn-secondary" onClick={addPassengerRow}>+ Add Passenger</button>
                )}
              </div>

              <button type="submit" className="btn btn-primary btn-lg" disabled={submitting}>
                {submitting ? 'Booking...' : `Confirm Booking — ₹${totalFare.toLocaleString('en-IN')}`}
              </button>
            </form>
          )}
        </>
      )}
    </div>
  );
}

export default BookingPage;
