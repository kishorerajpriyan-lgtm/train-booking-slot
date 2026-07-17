import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// ─── Stations ────────────────────────────────────────────────────────────────

export const getAllStations = () => api.get('/stations');

// ─── Trains ──────────────────────────────────────────────────────────────────

export const searchTrains = (origin, destination, date) =>
  api.get('/trains/search', { params: { origin, destination, travel_date: date } });

export const getTrain = (id) => api.get(`/trains/${id}`);

export const getTrainCoaches = (id, date) =>
  api.get(`/trains/${id}/coaches`, { params: { travel_date: date } });

// ─── Bookings ────────────────────────────────────────────────────────────────

export const createBooking = (data) => api.post('/bookings', data);

export const getBookingByPnr = (pnr) => api.get(`/bookings/pnr/${pnr}`);

export const getBookingsByEmail = (email) =>
  api.get('/bookings/', { params: { email } });

export const cancelBooking = (pnr) => api.put(`/bookings/${pnr}/cancel`);

export default api;
