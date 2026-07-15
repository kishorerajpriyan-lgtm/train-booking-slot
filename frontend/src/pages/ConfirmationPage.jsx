import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getBookingByPnr } from '../api';

function ConfirmationPage() {
  const { pnr } = useParams();
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBooking = async () => {
      try {
        setLoading(true);
        const res = await getBookingByPnr(pnr);
        setBooking(res.data);
      } catch (err) {
        setError('Failed to load booking details.');
      } finally {
        setLoading(false);
      }
    };
    fetchBooking();
  }, [pnr]);

  if (loading) return <div className="loading">Loading booking details...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!booking) return null;

  return (
    <div className="confirmation-page">
      <div className="confirmation-header">
        <div className="success-icon">✅</div>
        <h2>Booking Confirmed!</h2>
        <p className="pnr-display">
          Your PNR: <strong>{booking.pnr}</strong>
        </p>
      </div>

      <div className="booking-details-card">
        <h3>Booking Details</h3>
        <div className="detail-row">
          <span>Train</span>
          <span>
            {booking.train
              ? `${booking.train.train_name} (${booking.train.train_number})`
              : `Train #${booking.train_id}`}
          </span>
        </div>
        <div className="detail-row">
          <span>Route</span>
          <span>
            {booking.train
              ? `${booking.train.origin} → ${booking.train.destination}`
              : '—'}
          </span>
        </div>
        <div className="detail-row">
          <span>Travel Date</span>
          <span>{booking.travel_date}</span>
        </div>
        <div className="detail-row">
          <span>Class</span>
          <span>{booking.travel_class}</span>
        </div>
        <div className="detail-row">
          <span>Email</span>
          <span>{booking.email}</span>
        </div>
        <div className="detail-row">
          <span>Phone</span>
          <span>{booking.phone}</span>
        </div>
        <div className="detail-row">
          <span>Total Fare</span>
          <span>₹{booking.total_fare?.toLocaleString('en-IN')}</span>
        </div>
        <div className="detail-row">
          <span>Status</span>
          <span className="status-confirmed">{booking.status.toUpperCase()}</span>
        </div>
      </div>

      {booking.passengers?.length > 0 && (
        <div className="passenger-details">
          <h3>Passenger List</h3>
          <table className="passenger-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Name</th>
                <th>Age</th>
                <th>Gender</th>
                <th>Seat Preference</th>
              </tr>
            </thead>
            <tbody>
              {booking.passengers.map((p, i) => (
                <tr key={p.id}>
                  <td>{i + 1}</td>
                  <td>{p.name}</td>
                  <td>{p.age}</td>
                  <td>{p.gender}</td>
                  <td>{p.seat_preference}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="confirmation-actions">
        <Link to="/" className="btn btn-primary">Book Another</Link>
        <Link to="/my-bookings" className="btn btn-secondary">View My Bookings</Link>
      </div>
    </div>
  );
}

export default ConfirmationPage;
