function PassengerForm({ index, passenger, onChange, onRemove, showRemove }) {
  const handleChange = (field, value) => {
    onChange(index, { ...passenger, [field]: value });
  };

  return (
    <div className="passenger-form">
      <div className="passenger-header">
        <h4>Passenger {index + 1}</h4>
        {showRemove && (
          <button
            type="button"
            className="btn btn-danger-sm"
            onClick={() => onRemove(index)}
          >
            ✕ Remove
          </button>
        )}
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Name</label>
          <input
            type="text"
            value={passenger.name}
            onChange={(e) => handleChange('name', e.target.value)}
            placeholder="Full name"
            required
          />
        </div>

        <div className="form-group">
          <label>Age</label>
          <input
            type="number"
            value={passenger.age}
            onChange={(e) => handleChange('age', parseInt(e.target.value) || '')}
            min="1"
            max="120"
            placeholder="Age"
            required
          />
        </div>

        <div className="form-group">
          <label>Gender</label>
          <select
            value={passenger.gender}
            onChange={(e) => handleChange('gender', e.target.value)}
            required
          >
            <option value="">Select</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div className="form-group">
          <label>Seat Preference</label>
          <select
            value={passenger.seat_preference}
            onChange={(e) => handleChange('seat_preference', e.target.value)}
          >
            <option value="No Preference">No Preference</option>
            <option value="Window">Window</option>
            <option value="Aisle">Aisle</option>
          </select>
        </div>
      </div>
    </div>
  );
}

export default PassengerForm;
