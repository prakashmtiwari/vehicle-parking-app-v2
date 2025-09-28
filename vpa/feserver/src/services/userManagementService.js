import axios from "axios"

const API_BASE_URL = "http://127.0.0.1:5000/admin/users"

// Helper: get token from localStorage (or Pinia/Vuex store)
function authHeader() {
  const token = localStorage.getItem("token")
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
