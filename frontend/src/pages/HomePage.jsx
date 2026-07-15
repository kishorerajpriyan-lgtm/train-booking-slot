import { useNavigate } from 'react-router-dom';
import SearchForm from '../components/SearchForm';

function HomePage() {
  const navigate = useNavigate();

  const handleSearch = ({ origin, destination, date, travelClass }) => {
    navigate(
      `/search?origin=${origin}&destination=${destination}&date=${date}&class=${travelClass}`
    );
  };

  return (
    <div className="home-page">
      <div className="hero">
        <h1>Train Ticket Booking</h1>
        <p>Search and book train tickets across India — fast, simple, no login required.</p>
      </div>
      <SearchForm onSearch={handleSearch} />
    </div>
  );
}

export default HomePage;
