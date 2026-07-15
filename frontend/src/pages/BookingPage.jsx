import { useState, useEffect } from 'react';
import { useParams, useSearchParams, useNavigate } from 'react-router-dom';
import { getTrain, createBooking } from '../api';
import PassengerForm from '../components/PassengerForm';

const emptyPassenger = {
  name: '',
  age: '',
  gender: '',
  seat_preference: 'No Preference',
};

function BookingPage() {
  const { trainId } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const travelClass = searchParams.get('class') || 'Sleeper';
  const travelDate = searchParams.get('date') || '';

  const [train, setTrain] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [passengers, setPassengers] = useState([{ ...emptyPassenger }]);

  const farePerPassenger = train
    ? travelClass === 'AC'
      ? train.ac_fare
      : train.sleeper_fare
    : 0;
  const totalFare = farePerPassenger * passengers.length;

  useEffect(() => {
    const fetchTrain = async () => {
      try {
        setLoading(true);
        const res = await getTrain(trainId);
        setTrain(res.data);
      } catch (err) {
        setError('Failed to load train details.');
      } finally {
        setLoading(false);
      }
    };
    fetchTrain();
  }, [trainId]);

  const handlePassengerChange = (index, updated) => {
    const updatedList = [...passengers];
    updatedList[index] = updated;
    setPassengers(updatedList);
  };

  const addPassenger = () => {
    if (passengers.length >= 6) {
      alert('Maximum 6 passengers allowed');
      return;
    }
    setPassengers([...passengers, { ...emptyPassenger }]);
  };

  const removePassenger = (index) => {
    if (passengers.length <= 1) return;
    setPassengers(passengers.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate
    if (!email || !phone) {
      alert('Please fill contact details');
      return;
    }
    for (let i = 0; i < passengers.length; i++) {
      const p = passengers[i];
      if (!p.name || !p.age || !p.gender) {
        alert(`Please fill all details for Passenger ${i + 1}`);
        return;
      }
    }

    const bookingData = {
      train_id: parseInt(trainId),
      travel_date: travelDate,
      travel_class: travelClass,
      email,
      phone,
      passengers: passengers.map((p) => ({
        name: p.name,
        age: p.age,
        gender: p.gender,
        seat_preference: p.seat_preference,
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

  if (loading) return <div className="loading">Loading train details...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!train) return null;

  return (
    <div className="booking-page">
      <h2>Complete Your Booking</h2>

      {/* Train Summary */}
      <div className="booking-train-summary">
        <h3>
          {train.train_name} ({train.train_number})
        </h3>
        <p>
          {train.origin} → {train.destination} | {travelDate} | {travelClass} Class | ₹
          {farePerPassenger.toLocaleString('en-IN')}/person
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Contact Info */}
        <div className="contact-section">
          <h3>Contact Details</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                required
              />
            </div>
            <div className="form-group">
              <label>Phone</label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="9876543210"
                required
              />
            </div>
          </div>
        </div>

        {/* Passengers */}
        <div className="passengers-section">
          <h3>Passengers</h3>
          {passengers.map((p, i) => (
            <PassengerForm
              key={i}
              index={i}
              passenger={p}
              onChange={handlePassengerChange}
              onRemove={removePassenger}
              showRemove={passengers.length > 1}
            />
          ))}

          <button
            type="button"
            className="btn btn-secondary"
            onClick={addPassenger}
            disabled={passengers.length >= 6}
          >
            + Add Passenger
          </button>
        </div>

        {/* Fare Summary */}
        <div className="fare-summary">
          <h3>Fare Summary</h3>
          <div className="fare-row">
            <span>
              {farePerPassenger.toLocaleString('en-IN')} × {passengers.length} passenger(s)
            </span>
            <span>₹{totalFare.toLocaleString('en-IN')}</span>
          </div>
          <div className="fare-row total">
            <strong>Total</strong>
            <strong>₹{totalFare.toLocaleString('en-IN')}</strong>
          </div>
        </div>

        <button type="submit" className="btn btn-primary btn-lg" disabled={submitting}>
          {submitting ? 'Booking...' : `Confirm Booking — ₹${totalFare.toLocaleString('en-IN')}`}
        </button>
      </form>
    </div>
  );
}

export default BookingPage;
