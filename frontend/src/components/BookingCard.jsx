function BookingCard({ booking, onCancel }) {
  const isCancelled = booking.status === 'cancelled';
  const trainName = booking.train
    ? `${booking.train.train_name} (${booking.train.train_number})`
    : `Train #${booking.train_id}`;
  const route = booking.train
    ? `${booking.train.origin} → ${booking.train.destination}`
    : '';

  return (
    <div className={`booking-card ${isCancelled ? 'cancelled' : ''}`}>
      <div className="booking-card-header">
        <div>
          <span className="pnr">PNR: {booking.pnr}</span>
          <span className={`status-badge ${booking.status}`}>
            {booking.status.toUpperCase()}
          </span>
        </div>
        {!isCancelled && (
          <button
            className="btn btn-danger-sm"
            onClick={() => onCancel(booking.pnr)}
          >
            Cancel Booking
          </button>
        )}
      </div>

      <div className="booking-card-body">
        <div className="booking-detail">
          <span className="label">Train</span>
          <span>{trainName}</span>
        </div>
        <div className="booking-detail">
          <span className="label">Route</span>
          <span>{route}</span>
        </div>
        <div className="booking-detail">
          <span className="label">Travel Date</span>
          <span>{booking.travel_date}</span>
        </div>
        <div className="booking-detail">
          <span className="label">Class</span>
          <span>{booking.travel_class}</span>
        </div>
        <div className="booking-detail">
          <span className="label">Total Fare</span>
          <span>₹{booking.total_fare?.toLocaleString('en-IN')}</span>
        </div>
      </div>

      {booking.passengers?.length > 0 && (
        <div className="passenger-list">
          <h5>Passengers:</h5>
          <ul>
            {booking.passengers.map((p) => (
              <li key={p.id}>
                {p.name} ({p.age}, {p.gender})
                {p.booked_seat && (
                  <span className="seat-info">
                    {' '}— {p.booked_seat.coach_code}/{p.booked_seat.seat_number} ({p.booked_seat.berth_type})
                  </span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default BookingCard;
