import axios from "axios"

const API_BASE_URL = "http://localhost:5000/api/reservations" // Main reservations endpoint
const API_USER_BASE_URL = "http://localhost:5000/api/myreservations" // 

function authHeader() {
  const token = localStorage.getItem("token")
  return token ? { Authorization: `Bearer ${token}` } : {}
}


export default {
  // ✅ Get reservations for a specific user
  getUserReservations() {
    return axios.get(`${API_USER_BASE_URL}`, {
      headers: authHeader(),
    })
  },

  // ✅ Get reservation by ID
  getReservation(reservationId) {
    return axios.get(`${API_BASE_URL}/${reservationId}`, {
      headers: authHeader(),
    })
  },

  // ✅ Create a new reservation
  createReservation(data) {
    return axios.post(API_USER_BASE_URL, data, {
      headers: authHeader(),
    })
  },

  // ✅ Update an existing reservation (e.g., extend time)
  updateReservation(reservationId, data) {
    return axios.put(`${API_BASE_URL}/${reservationId}`, data, {
      headers: authHeader(),
    })
  },

  // ✅ Cancel / delete a reservation
  deleteReservation(reservationId) {
    return axios.delete(`${API_BASE_URL}/${reservationId}`, {
      headers: authHeader(),
    })
  },

  // ✅ Free a parking spot (custom endpoint, if implemented)
  freeSpot(reservationId) {
    return axios.post(`${API_BASE_URL}/${reservationId}/free`, {}, {
      headers: authHeader(),
    })
  }
}
