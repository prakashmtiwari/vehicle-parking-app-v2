import axios from "axios"
import { useAuthStore } from '@/stores/auth'
import { API_HOST } from './apiConfig'

const API_BASE_URL = `${API_HOST}/api/reservations` // Main reservations endpoint
const API_USER_BASE_URL = `${API_HOST}/api/myreservations` // 
const API_EXPORT_URL = `${API_HOST}/api/export-history` // Export history endpoint



export function authHeader() {
  const auth = useAuthStore()

  // Get the token either from the store (preferred)
  // or from localStorage as fallback
  let token = auth.token

  // Fallback: if the store is not initialized yet (e.g., on page reload)
  if (!token && auth.user?.username) {
    token = localStorage.getItem(`token_${auth.user.username}`)
  }

  return token ? { Authorization: `Bearer ${token}` } : {}
}


export default {

  getAllReservations() {
    return axios.get(`${API_BASE_URL}`, {
      headers: authHeader(),
    })
  },

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

  // ✅ Cancel a reservation by the user
  cancelReservation(reservationId) {
    return axios.delete(`${API_USER_BASE_URL}/${reservationId}`, {
      headers: authHeader(),
    })
  },

  // ✅ Complete a  reservation by paying and freeing the spot
  completeReservation(reservationId) {
    return axios.post(`${API_USER_BASE_URL}/${reservationId}`, {}, {
      headers: authHeader(),
    })
  },
  // ✅ Export user parking history 
  exportUserHistory() {
    return axios.post(`${API_EXPORT_URL}`, {}, {
      headers: authHeader(),
    })
  },
  getParkingAmount(reservationId){
    return axios.get(`${API_USER_BASE_URL}/${reservationId}`, {
       headers: authHeader(),
    })
  }


} 
