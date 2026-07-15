import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">🚂 TrainBooking</Link>
      </div>
      <div className="navbar-links">
        <Link to="/">Home</Link>
        <Link to="/my-bookings">My Bookings</Link>
      </div>
    </nav>
  );
}

export default Navbar;
