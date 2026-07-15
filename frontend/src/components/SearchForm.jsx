import { useState, useEffect, useRef } from 'react';
import { getAllStations } from '../api';

function SearchForm({ onSearch }) {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [date, setDate] = useState('');
  const [travelClass, setTravelClass] = useState('Sleeper');
  const [stations, setStations] = useState([]);
  const [originFilter, setOriginFilter] = useState([]);
  const [destFilter, setDestFilter] = useState([]);
  const [showOriginDropdown, setShowOriginDropdown] = useState(false);
  const [showDestDropdown, setShowDestDropdown] = useState(false);
  const originRef = useRef(null);
  const destRef = useRef(null);

  useEffect(() => {
    const fetchStations = async () => {
      try {
        const res = await getAllStations();
        setStations(res.data);
      } catch (err) {
        console.error('Failed to load stations:', err);
      }
    };
    fetchStations();
  }, []);

  useEffect(() => {
    const handleClick = (e) => {
      if (originRef.current && !originRef.current.contains(e.target)) {
        setShowOriginDropdown(false);
      }
      if (destRef.current && !destRef.current.contains(e.target)) {
        setShowDestDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const handleOriginInput = (value) => {
    setOrigin(value);
    if (value.length >= 1) {
      const filtered = stations.filter(
        (s) =>
          s.code.toLowerCase().includes(value.toLowerCase()) ||
          s.name.toLowerCase().includes(value.toLowerCase())
      );
      setOriginFilter(filtered.slice(0, 8));
      setShowOriginDropdown(true);
    } else {
      setOriginFilter([]);
      setShowOriginDropdown(false);
    }
  };

  const handleDestInput = (value) => {
    setDestination(value);
    if (value.length >= 1) {
      const filtered = stations.filter(
        (s) =>
          s.code.toLowerCase().includes(value.toLowerCase()) ||
          s.name.toLowerCase().includes(value.toLowerCase())
      );
      setDestFilter(filtered.slice(0, 8));
      setShowDestDropdown(true);
    } else {
      setDestFilter([]);
      setShowDestDropdown(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!origin || !destination || !date) {
      alert('Please fill all fields');
      return;
    }
    // Extract just the code for the search
    const originCode = origin.includes(' - ') ? origin.split(' - ')[0] : origin.toUpperCase();
    const destCode = destination.includes(' - ') ? destination.split(' - ')[0] : destination.toUpperCase();
    onSearch({ origin: originCode, destination: destCode, date, travelClass });
  };

  const today = new Date().toISOString().split('T')[0];

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <h2>Search Trains</h2>
      <div className="form-row">
        <div className="form-group" ref={originRef}>
          <label>From Station</label>
          <input
            type="text"
            value={origin}
            onChange={(e) => handleOriginInput(e.target.value)}
            onFocus={() => origin.length >= 1 && setShowOriginDropdown(true)}
            placeholder="Station code or name (e.g., NDLS, Delhi)"
            required
            autoComplete="off"
          />
          {showOriginDropdown && originFilter.length > 0 && (
            <ul className="station-dropdown">
              {originFilter.map((s) => (
                <li
                  key={s.code}
                  onClick={() => {
                    setOrigin(`${s.code} - ${s.name}`);
                    setShowOriginDropdown(false);
                  }}
                >
                  <strong>{s.code}</strong> — {s.name} <small>({s.state})</small>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="form-group" ref={destRef}>
          <label>To Station</label>
          <input
            type="text"
            value={destination}
            onChange={(e) => handleDestInput(e.target.value)}
            onFocus={() => destination.length >= 1 && setShowDestDropdown(true)}
            placeholder="Station code or name"
            required
            autoComplete="off"
          />
          {showDestDropdown && destFilter.length > 0 && (
            <ul className="station-dropdown">
              {destFilter.map((s) => (
                <li
                  key={s.code}
                  onClick={() => {
                    setDestination(`${s.code} - ${s.name}`);
                    setShowDestDropdown(false);
                  }}
                >
                  <strong>{s.code}</strong> — {s.name} <small>({s.state})</small>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="form-group">
          <label>Travel Date</label>
          <input
            type="date"
            value={date}
            min={today}
            onChange={(e) => setDate(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Class</label>
          <select value={travelClass} onChange={(e) => setTravelClass(e.target.value)}>
            <option value="Sleeper">Sleeper</option>
            <option value="AC">AC</option>
          </select>
        </div>
      </div>

      <button type="submit" className="btn btn-primary">Search Trains</button>
    </form>
  );
}

export default SearchForm;
