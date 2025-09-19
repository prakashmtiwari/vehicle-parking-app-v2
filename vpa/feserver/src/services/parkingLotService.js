import axios from "axios"

const API_URL = "http://127.0.0.1:5000/admin/lots"

// Helper: get token from localStorage (or Pinia/Vuex store)
function authHeader() {
  const token = localStorage.getItem("token")
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export default {
  async getLots() {
    return axios.get(API_URL, { headers: authHeader() })
  },

  async createLot(data) {
    return axios.post(API_URL, data, { headers: authHeader() })
  },

  async updateLot(id, data) {
    return axios.put(`${API_URL}/${id}`, data, { headers: authHeader() })
  },

  async deleteLot(id) {
    return axios.delete(`${API_URL}/${id}`, { headers: authHeader() })
  },

  async getSpots(lotId) {
    return axios.get(`${API_URL}/${lotId}/spots`, { headers: authHeader() })
  }
}
