import axios from "axios"
import { useAuthStore } from '@/stores/auth'


const API_URL = "http://127.0.0.1:5000/api/lots"


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
