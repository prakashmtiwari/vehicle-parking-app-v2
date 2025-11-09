import axios from "axios"
import { useAuthStore } from '@/stores/auth'


const API_EXPORT_URL = "http://localhost:5000/api/export-history" // Export history endpoint
const API_STATUS_URL = "http://localhost:5000/api/export-status" // Export status endpoint


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

  triggerExport() {
    return axios.post(`${API_EXPORT_URL}`, null,{
      headers: authHeader(),
    })
  },
  
  exportStatus(jobId) {
    return axios.get(`${API_STATUS_URL}/${jobId}`, {
      headers: authHeader(),
    })
  }
}