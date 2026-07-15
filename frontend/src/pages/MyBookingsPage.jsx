import { useState } from 'react';
import { getBookingsByEmail, cancelBooking } from '../api';
import BookingCard from '../components/BookingCard';

function MyBookingsPage() {
  const [email, setEmail] = useState('');
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!email) return;

    try {
      setLoading(true);
      setError('');
      setSearched(true);
      const res = await getBookingsByEmail(email);
      setBookings(res.data);
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Failed to fetch bookings.'
      );
      setBookings([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (pnr) => {
    if (!window.confirm('Are you sure you want to cancel this booking?')) return;

    try {
      await cancelBooking(pnr);
      // Refresh the list
      const res = await getBookingsByEmail(email);
      setBookings(res.data);
      alert('Booking cancelled successfully.');
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to cancel booking.');
    }
  };

  return (
    <div className="my-bookings-page">
      <h2>My Bookings</h2>
      <p>Enter your email to view your bookings.</p>

      <form className="email-search-form" onSubmit={handleSearch}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email address"
          required
        />
        <button type="submit" className="btn btn-primary">Search</button>
      </form>

      {loading && <div className="loading">Loading bookings...</div>}

      {error && <div className="error-message">{error}</div>}

      {searched && !loading && !error && bookings.length === 0 && (
        <div className="no-results">No bookings found for this email.</div>
      )}

      <div className="bookings-list">
        {bookings.map((booking) => (
          <BookingCard
            key={booking.id}
            booking={booking}
            onCancel={handleCancel}
          />
        ))}
      </div>
    </div>
  );
}

export default MyBookingsPage;
