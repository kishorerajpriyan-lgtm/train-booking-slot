import { useNavigate } from 'react-router-dom';

function TrainCard({ train, travelClass, travelDate }) {
  const navigate = useNavigate();

  const fare = travelClass === 'AC' ? train.ac_fare : train.sleeper_fare;
  const available =
    travelClass === 'AC' ? train.available_ac_seats : train.available_sleeper_seats;

  const handleBook = () => {
    navigate(`/book/${train.id}?class=${travelClass}&date=${travelDate}`);
  };

  return (
    <div className="train-card">
      <div className="train-card-header">
        <h3>{train.train_name}</h3>
        <span className="train-number">{train.train_number}</span>
      </div>

      <div className="train-card-body">
        <div className="train-route">
          <div className="station">
            <span className="station-code">{train.origin}</span>
            <span className="station-time">{train.departure_time}</span>
          </div>
          <div className="route-line">
            <span>{train.duration_hours}h</span>
          </div>
          <div className="station">
            <span className="station-code">{train.destination}</span>
            <span className="station-time">{train.arrival_time}</span>
          </div>
        </div>

        <div className="train-details">
          <div className="detail">
            <span className="detail-label">Class</span>
            <span className="detail-value">{travelClass}</span>
          </div>
          <div className="detail">
            <span className="detail-label">Fare</span>
            <span className="detail-value">₹{fare.toLocaleString('en-IN')}</span>
          </div>
          <div className="detail">
            <span className="detail-label">Seats Left</span>
            <span className={`detail-value ${available < 10 ? 'low-seats' : ''}`}>
              {available}
            </span>
          </div>
        </div>
      </div>

      <button
        className="btn btn-primary"
        onClick={handleBook}
        disabled={available === 0}
      >
        {available === 0 ? 'Sold Out' : 'Book Now'}
      </button>
    </div>
  );
}

export default TrainCard;
