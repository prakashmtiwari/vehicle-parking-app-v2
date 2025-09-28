import axios from "axios"

const API_URL = "http://127.0.0.1:5000/api/lots"

// Helper: get token from localStorage (or Pinia/Vuex store)
function authHeader() {
  const token = localStorage.getItem("token")
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export default {
  async getLots() {
    return axios.get(API_URL, { headers: authHeader() })
  },

  async getLot(id) {
    return axios.get(`${API_URL}/${id}`, { headers: authHeader() })
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
  },
  
  // method to release spot

  async releaseSpot(spotId) {
    return axios.post(
      `${API_BASE_URL}/spots/${spotId}/release`,
      {},
      { headers: authHeader() }
    )
  },

// Fetch all lots with their associated spots
  async getLotsWithSpots() {
  const lotsRes = await this.getLots()
  console.log("Fetched lots:", lotsRes.data)
  const lots = lotsRes.data

  // Fetch spots for each lot
  const lotsWithSpots = await Promise.all(
    lots.map(async (lot) => {
      try {
        const spotsRes = await this.getSpots(lot.id)
        return { ...lot, spots: spotsRes.data }
      } catch (err) {
        console.error(`Failed to fetch spots for lot ${lot.id}`, err)
        return { ...lot, spots: [] }
      }
    })
  )

  return { data: lotsWithSpots }
}

}
