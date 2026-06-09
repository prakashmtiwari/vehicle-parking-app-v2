import axios from "axios"
import { useAuthStore } from '@/stores/auth'
import { API_HOST } from './apiConfig'

const API_BASE_URL = `${API_HOST}/admin/users`


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
  // Get all users
  getUsers() {
    return axios.get(API_BASE_URL, { headers: authHeader() })
  },

  // Get a single user by ID
  getUser(id) {
    return axios.get(`${API_BASE_URL}/${id}`, { headers: authHeader() })
  },

  // Update an existing user
  updateUser(id, data) {
    // data can include { username, email, password, role }
    return axios.put(`${API_BASE_URL}/${id}`, data, { headers: authHeader() })
  },

  // Delete a user by ID
  deleteUser(id) {
    return axios.delete(`${API_BASE_URL}/${id}`, { headers: authHeader() })
  }
}
