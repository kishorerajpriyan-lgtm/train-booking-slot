import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { searchTrains } from '../api';
import TrainCard from '../components/TrainCard';

function SearchResultsPage() {
  const [searchParams] = useSearchParams();
  const [trains, setTrains] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const origin = searchParams.get('origin') || '';
  const destination = searchParams.get('destination') || '';
  const date = searchParams.get('date') || '';
  const travelClass = searchParams.get('class') || 'Sleeper';

  useEffect(() => {
    const fetchTrains = async () => {
      try {
        setLoading(true);
        setError('');
        const res = await searchTrains(origin, destination, date);
        setTrains(res.data);
      } catch (err) {
        if (err.response?.status === 404) {
          setTrains([]);
        } else {
          setError(
            err.response?.data?.detail || 'Failed to search trains. Please try again.'
          );
          setTrains([]);
        }
      } finally {
        setLoading(false);
      }
    };

    if (origin && destination && date) {
      fetchTrains();
    }
  }, [origin, destination, date]);

  return (
    <div className="search-results-page">
      <div className="search-summary">
        <h2>
          {origin} → {destination}
        </h2>
        <p>
          {date} | {travelClass} Class
        </p>
      </div>

      {loading && <div className="loading">Searching trains...</div>}

      {error && <div className="error-message">{error}</div>}

      {!loading && !error && trains.length === 0 && (
        <div className="no-results-card">
          <div className="no-results-icon">🔍</div>
          <h3>No Trains Found</h3>
          <p>
            No trains available from {origin} to {destination} on {date}.
          </p>
          <p className="no-results-hint">
            Try a different date, route, or station pair. Not all station pairs may have direct trains.
          </p>
        </div>
      )}

      <div className="train-list">
        {trains.map((train) => (
          <TrainCard key={train.id} train={train} travelClass={travelClass} travelDate={date} />
        ))}
      </div>
    </div>
  );
}

export default SearchResultsPage;
